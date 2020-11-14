import json
import logging
from datetime import datetime, timedelta, timezone
from os import listdir

import requests

from common import dispatch

logging.basicConfig(filename='logs/meetup.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

api_base_url = 'https://api.meetup.com'

blacklist_filename = 'static/meetup_blacklist.json'
groups_filename = 'static/meetup_groups.json'
state_filename = 'state/meetup_state.json'

additional_fields = ','.join([
    'plain_text_no_images_description',
    'featured_photo'
])

def init_state_file() -> None:
    """
        Create crawler state file if it doesn't exist
    """

    if state_filename not in listdir('.'):
        logging.info('Crawler started at the first time')

        with open(state_filename, 'w') as handle:
            handle.write('{}')

def load_timestamp(group: str) -> int:
    """
        Load creation timestamp of last created event of provided group
    """

    logging.info('Loading timestamp of group {}'.format(group))

    with open(state_filename) as handle:
        return json.load(handle).get(group, 0)

def save_timestamp(group: str, timestamp: int) -> None:
    """
        Save creation timestamp of last created event of provided group
    """

    logging.info('Saving timestamp of group {}'.format(group))

    with open(state_filename, 'r') as handle:
        obj = json.load(handle)

    obj.update({group: timestamp})

    with open(state_filename, 'w') as handle:
        json.dump(obj, handle)

def get_groups() -> list:
    """
        Get list of groups to collect events from
    """

    logging.info('Groups list loaded')

    with open(groups_filename, 'r', encoding='utf8') as handle:
        return json.load(handle)

# Because there are too much same events of that groups
# They differ only in the date
def get_group_blacklist() -> list:
    """
        Get urlnames of groups that are in blacklist
    """

    with open(blacklist_filename, 'r') as handle:
        return json.load(handle)

def extract_info(event: dict) -> dict:
    """
        Extract only fields we have to store from raw event provided
    """

    timestamp = event['time'] // 1000
    event_time = datetime.utcfromtimestamp(timestamp)

    venue = event.get('venue', dict())

    if event['is_online_event']:
        city = 'Без города'
        place = 'Online event'
    else:
        city = venue.get('city', None)

        address = (
            venue.get('name', None),
            venue.get('address_1', None),
            venue.get('address_2', None),
            venue.get('address_3', None)
        )

        place = ', '.join(x for x in address
                          if x is not None)
        place = place or None

    categories = ['Tech']

    logo_path = event.get('featured_photo', dict()) \
                     .get('highres_link', None)

    return {
        'name': event['name'],
        'event_type': None,
        'event_time': event_time,
        'city': city,
        'place': place,
        'source_url': event['link'],
        'description': event['plain_text_no_images_description'],
        'categories': categories,
        'logo_path': logo_path
    }

def get_events() -> None:
    """
        Store events that have been created since last launch in database
    """

    base_url = api_base_url + '/{urlname}/events'

    group_blacklist = get_group_blacklist()
    groups = get_groups()

    for group in groups:
        urlname = group['urlname']

        if urlname in group_blacklist:
            continue

        url = base_url.format(urlname=urlname)

        last_create_timestamp = load_timestamp(urlname)
        new_create_timestamp = last_create_timestamp

        params = {
            'fields': additional_fields,
            'status': 'upcoming'
        }

        response = requests.get(url, params=params).json()
        events_num = len(response)

        logging.info('Loaded %d upcoming events of group %s' % (events_num,
                                                                urlname))

        for event in response:
            if event['created'] <= last_create_timestamp:
                continue

            dispatch(extract_info(event))

            new_create_timestamp = max(new_create_timestamp,
                                       event['created'])

        save_timestamp(urlname, new_create_timestamp)

if __name__ == '__main__':
    init_state_file()
    get_events()
