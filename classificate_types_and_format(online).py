def classificate_types_and_format(csv_in, csv_out):
    import pandas
    import numpy as np
    pandas.options.mode.chained_assignment = None

    events_df = pandas.read_csv(csv_in)
    # events_df['type'] = np.nan

    hackathon = ['hackathon', 'хакатон', 'Конкурс']
    webinar = ['webinar', 'вебинар', 'lecture', 'лекция', 'Вебинар', 'Лекция']
    conference = ['conference', 'конференция', 'Конференция']
    training = ['training', 'тренинг', 'семинар', 'workshop', 'мастер класс', 'воркшоп', 'Тренинг']
    course = [r'\bcourse\b', r'\bкурс\b']
    meetup = ['meetup', 'митап', 'Митап']
    olympiad = ['olympiad', 'олимпиада']

    types = ['hackathon', 'webinar', 'conference', 'training', 'course', 'meetup', 'olympiad', 'others']
    keywords = [hackathon, webinar, conference, training, course, meetup, olympiad]

    online = ['Без города', 'без города', 'online', 'онлайн', 'Online', 'Онлайн', 'Internet', 'internet', 'Интернет', 'интернет']

    for i in range(len(events_df)):
        descr = events_df['normalized_description'][i]
        name = events_df['normalized_name'][i]
        type = events_df['event_type'][i]
        city = events_df['city'][i]
        if pandas.isna(city) or any(word in city for word in online):
            events_df['city'][i] = 'online'
        for j in range(len(keywords)):
            if any(word in type for word in keywords[j]):
                events_df['event_type'][i] = types[j]
            elif any(word in name for word in keywords[j]):
                events_df['event_type'][i] = types[j]
            elif not pandas.isna(descr):
                if any(word in descr for word in keywords[j]):
                    events_df['event_type'][i] = types[j]
    events_df['event_type'] = events_df['event_type'].fillna(types[-1])

    events_df.to_csv(csv_out, index=False, index_label=False)
