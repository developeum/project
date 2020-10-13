from utils.db_worker import store_event, commit_changes
from config import TIMEPAD_API_TOKEN
from datetime import timedelta
from datetime import timezone
from datetime import datetime
import requests, os, logging

logging.basicConfig(filename='.timepad.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

api_base_url = 'https://api.timepad.ru'
events_url = api_base_url + '/v1/events'

session = requests.Session()
session.headers.update({
    'Authorization': 'Bearer {token}'.format(token=TIMEPAD_API_TOKEN)
})

fields = ','.join([
    'name', 'starts_at',
    'description_short',
    'location', 'url',
    'categories',
    'poster_image',
    'created_at'
])

def update_timestamp():
    """
        Return last launch timestamp and save current one
    """

    last_update_filename = '.last_update_timepad'
    week_as_secs = 7 * 24 * 60 * 60

    current_timestamp = int(datetime.now().timestamp())

    if last_update_filename not in os.listdir('.'):
        logging.info('Crawler launched at the first time')
        last_launch_timestamp = current_timestamp - 2*week_as_secs
    else:
        logging.info('Got last launch timestamp')
        with open(last_update_filename, 'r') as handle:
            last_launch_timestamp = int(handle.read().strip())

    logging.info('Last launch time updated')
    with open(last_update_filename, 'w') as handle:
        handle.write(str(current_timestamp))

    return last_launch_timestamp

def get_events():
    """
        Store events that has been created since last launch in database
    """

    # Get last update timestamp and save current one
    time_template = '%Y-%m-%dT%H:%M:%S%z'
    delta = timedelta(hours=3)
    limit = 100

    timestamp = update_timestamp()

    last_update_obj = datetime.utcfromtimestamp(timestamp) + delta
    last_update_obj = last_update_obj.astimezone(timezone(delta))
    last_update_str = last_update_obj.strftime(time_template)

    params = {
        'fields': fields,
        'limit': limit,
        'moderation_statuses': 'featured',
        'sort': '-created_at',
        'created_at_min': last_update_str,
        'skip': 0,
    }

    # Get events since that time
    total = limit + 1

    while total > limit:
        response = session.get(events_url, params=params).json()

        total = response['total'] - params['skip']
        events = response['values']

        logging.info('Got %d events, %d remaining' % (len(events), total))

        for event in events:
            name = event.get('name')

            event_time = datetime.strptime(event.get('starts_at'),
                                           time_template)

            location = event.get('location', dict())
            
            city = location.get('city', None)
            place = location.get('address', None)

            url = event.get('url', None)
            description = event.get('description_short', None)

            categories_raw = event.get('categories', [])
            categories = [item['name'] for item in categories_raw]

            logo_path = event.get('poster_image', dict()) \
                             .get('default_url', None)

            store_event(name, event_time, city, place, url,
                        description, categories, logo_path)

        params['skip'] += limit

    commit_changes()

if __name__ == '__main__':
    get_events()
