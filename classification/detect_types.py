import pandas as pd

def Detect_type(csv_in, csv_out):
    pd.options.mode.chained_assignment = None

    events_df = pd.read_csv(csv_in)

    hackathon = ['hackathon', 'хакатон', 'Конкурс']
    webinar = ['webinar', 'вебинар', 'lecture', 'лекция', 'Вебинар', 'Лекция']
    conference = ['conference', 'конференция', 'Конференция']
    training = ['training', 'тренинг', 'семинар', 'workshop', 'мастер класс', 'воркшоп', 'Тренинг']
    course = [r'\bcourse\b', r'\bкурс\b']
    meetup = ['meetup', 'митап', 'Митап']
    olympiad = ['olympiad', 'олимпиада']

    types = ['hackathon', 'webinar', 'conference', 'training', 'course', 'meetup', 'olympiad', 'others']
    keywords = [hackathon, webinar, conference, training, course, meetup, olympiad]

    online = ['Без города', 'без города', 'online', 'онлайн', 'Online', 'Онлайн', 'Internet', 'internet', 'Интернет',
              'интернет']

    for i in range(len(events_df)):
        descr = events_df['normalized_description'][i]
        name = events_df['normalized_name'][i]
        ev_type = events_df['event_type'][i]
        city = events_df['city'][i]
        if pd.isna(city) or any(word in city for word in online):
            events_df['city'][i] = 'online'
        for j in range(len(keywords)):
            if not pd.isna(ev_type):
                if any(word in ev_type for word in keywords[j]):
                    events_df['event_type'][i] = types[j]
            elif not pd.isna(name):
                if any(word in name for word in keywords[j]):
                    events_df['event_type'][i] = types[j]
            elif not pd.isna(descr):
                if any(word in descr for word in keywords[j]):
                    events_df['event_type'][i] = types[j]
    events_df['event_type'] = events_df['event_type'].fillna(types[-1])

    events_df.to_csv(csv_out, index=False, index_label=False)
