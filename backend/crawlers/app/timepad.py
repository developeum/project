import logging
from datetime import datetime, timedelta, timezone
from os import listdir
from typing import Optional

import requests

from config import TIMEPAD_API_TOKEN
from utils.db_worker import commit_changes, store_event

logging.basicConfig(filename='.timepad.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

api_base_url = 'https://api.timepad.ru'
events_url = api_base_url + '/v1/events'

state_filename = '.last_update_timepad'
time_template = '%Y-%m-%dT%H:%M:%S%z'

session = requests.Session()
session.headers.update({
    'Authorization': 'Bearer {token}'.format(token=TIMEPAD_API_TOKEN)
})

fields = ','.join([
    'name',
    'starts_at',
    'description_short',
    'location',
    'url',
    'categories',
    'poster_image',
    'created_at'
])

def init_state_file() -> None:
    """
        Create crawler state file if it doesn't exist
    """

    if state_filename not in listdir('.'):
        logging.info('Crawler started at the first time')

        with open(state_filename, 'w') as handle:
            current_timestamp = int(datetime.now().timestamp())
            week_as_secs = 7 * 24 * 60 * 60

            save_timestamp(current_timestamp - 4*week_as_secs)

def load_timestamp() -> int:
    """
        Load timestamp of last crawler start time
    """

    with open(state_filename, 'r') as handle:
        return int(handle.read().strip())

def save_timestamp(timestamp: Optional[int] = None) -> None:
    """
        Save provided timestamp as last crawler start time
        If no timestamp provided, use current timestamp
    """

    timestamp = timestamp or int(datetime.now().timestamp())

    with open(state_filename, 'w') as handle:
        handle.write(str(timestamp))

def extract_info(event: dict) -> dict:
    """
        Extract only fields we have to store from raw event provided
    """

    event_time = datetime.strptime(event.get('starts_at'),
                                   time_template)

    location = event.get('location', dict())

    categories_raw = event.get('categories', [])
    categories = [item['name'] for item in categories_raw]

    logo_path = event.get('poster_image', dict()) \
                     .get('uploadcare_url', None)

    return {
        'name': event.get('name'),
        'event_time': event_time,
        'city': location.get('city', None),
        'place': location.get('address', None),
        'source_url': event.get('url', None),
        'description': event.get('description_short', None),
        'categories': categories,
        'logo_path': logo_path
    }

def get_events() -> None:
    """
        Store events that have been created since last launch in database
    """

    # Get last update timestamp and save current one
    timestamp = load_timestamp()
    save_timestamp()

    delta = timedelta(hours=3)
    limit = 100

    last_update_obj = datetime.utcfromtimestamp(timestamp) + delta
    last_update_obj = last_update_obj.astimezone(timezone(delta))
    last_update_str = last_update_obj.strftime(time_template)

    params = {
        'fields': fields,
        'limit': limit,
        'moderation_statuses': 'featured',
        'sort': '-created_at',
        'created_at_min': last_update_str,
        # Only IT events
        'category_ids': '452',
        'skip': 0,
    }

    # Get events since that time
    remaining = 1

    while remaining > 0:
        response = session.get(events_url, params=params).json()

        events = response['values']
        events_num = len(events)

        remaining = response['total'] - params['skip'] - events_num

        logging.info('Loaded %d events, %d remaining' % (events_num,
                                                         remaining))

        for event in events:
            info = extract_info(event)
            store_event(**info)

        params['skip'] += limit

    commit_changes()

if __name__ == '__main__':
    init_state_file()
    get_events()
