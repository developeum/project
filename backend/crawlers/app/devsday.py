import requests
from datetime import datetime
from bs4 import BeautifulSoup
from utils.db_worker import store_event, commit_changes

url_base = 'https://devsday.ru/Event/FilterEvents/'

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

def extract_info(event: dict) -> dict:
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
        'event_time': event_time,
        'city': event['CityName'],
        'place': place,
        'source_url': details_url,
        'description': description,
        'categories': tags,
        'logo_path': logo_path,
        'event_type': event_types[event['Category']-1]
    }

params = {
    'SearchText': '',
    # Only Russian events
    'CountryId': 1,
    'IsArchived': True,
    'Page': 0
}

for page in range(100):
    print(page)

    response = requests.post(url_base, data=params)
    events = response.json()['Data']['Items']

    for event in events:
        info = extract_info(event)
        store_event(**info)

    params['Page'] += 1

commit_changes()
