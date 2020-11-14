import json
import logging
from datetime import datetime
from os import listdir
from typing import List

import requests
from bs4 import BeautifulSoup

from common import dispatch

url_base = 'https://devsday.ru/Event/FilterEvents/'

state_filename = 'devsday_state.json'

logging.basicConfig(filename='.devsday.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

event_types = [
    "Конференция",
    "Митинг",
    "Тренинг",
    "Митап",
    "Лекция",
    "Семинар",
    "Вебинар",
    "Конкурс",
    "Выставка",
    "Церемония",
    "Другое"
]

organizer_blacklist = [
    'ООО "Среда 31"'
]

def load_state() -> List[int]:
    """
        Load events handled on last crawler launch
    """

    logging.info('Crawler state loaded')

    with open(state_filename, 'r') as handle:
        return json.load(handle)

def dump_state(handled_events: List[int]) -> None:
    """
        Save already handled events into crawler state
    """

    logging.info('Crawler state saved')

    with open(state_filename, 'w') as handle:
        json.dump(handled_events, handle)

def init_state_file() -> None:
    """
        Create crawler state file if it doesn't exist
    """

    if state_filename not in listdir('.'):
        logging.info('Crawler started at the first time')

        with open(state_filename, 'w') as handle:
            handle.write('[]')

def extract_info(event: dict) -> dict:
    """
        Extract only fields we have to store from raw event provided
    """

    details_url = 'https://devsday.ru/event/details/%d' % event['EventId']

    raw_date = event['Start']
    event_timestamp = int(raw_date[6:-2]) // 1000
    event_time = datetime.utcfromtimestamp(event_timestamp)

    full_info = requests.get(details_url).text
    soup = BeautifulSoup(full_info, 'html.parser')

    place = soup.find('strong', string='Адрес проведения: ').next_sibling
    if place is not None:
        place = str(place)

    logo_path = soup.find('img', class_='publication-big-image')
    if logo_path is not None:
        logo_path = logo_path['src']
        if not logo_path.startswith('http'):
            logo_path = 'https://devsday.ru'+logo_path

    description = soup.find('div', class_='event-details-description')
    if description is not None:
        description = description.find_all(text=True)
        description = ' '.join(description)

    tags = [tag.text for tag in soup.find_all(class_='display-tag')]

    return {
        'name': event['Title'],
        'event_type': event_types[event['Category']-1],
        'event_time': event_time,
        'city': event['CityName'],
        'place': place,
        'source_url': details_url,
        'description': description,
        'categories': tags,
        'logo_path': logo_path
    }

def get_events() -> None:
    """
        Store events that have been created since last launch in database
    """

    params = {
        'SearchText': '',
        # Only Russian events
        'CountryId': 1,
        'IsArchived': False,
        'Page': 0
    }

    last_handled_events = load_state()
    handled_events = []

    has_more = True

    # For logging
    events = 0

    while has_more:
        response = requests.post(url_base, data=params).json()

        has_more = response['Data']['HasMore']
        events = response['Data']['Items']

        for event in events:
            if event['Organizer'] in organizer_blacklist:
                continue

            handled_events.append(event['EventId'])

            if event['EventId'] not in last_handled_events:
                dispatch(extract_info(event))
                events += 1

        params['Page'] += 1

    logging.info('%d new events from %d pages saved into database' % 
                 (events, params['Page']))

    dump_state(handled_events)

if __name__ == '__main__':
    init_state_file()
    get_events()
