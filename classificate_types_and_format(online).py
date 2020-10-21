import pandas
import numpy as np
pandas.options.mode.chained_assignment = None

events_df = pandas.read_csv('events18102020.csv')
events_df['type'] = np.nan

hackathon = ['hackathon', 'хакатон']
webinar = ['webinar', 'вебинар', 'lecture', 'лекция']
conference = ['conference', 'конференция']
training = ['training', 'тренинг', 'семинар', 'workshop', 'мастер класс']
course = ['course', 'курс']
meetup = ['meetup', 'митап']

types = ['hackathon', 'webinar', 'conference', 'training', 'course', 'meetup', 'others']
keywords = [hackathon, webinar, conference, training, course, meetup]

online = ['Без города', 'без города', 'online', 'онлайн', 'Online', 'Онлайн']

for i in range(len(events_df)):
    descr = events_df['description'][i]
    name = events_df['name'][i]
    city = events_df['city'][i]
    if pandas.isna(city) or any(word in city for word in online):
        events_df['city'][i] = 'online'
    for j in range(len(keywords)):
        if any(word in name for word in keywords[j]):
            events_df['type'][i] = types[j]
        elif not pandas.isna(descr):
            if any(word in descr for word in keywords[j]):
                events_df['type'][i] = types[j]
events_df['type'] = events_df['type'].fillna(types[-1])

events_df.to_csv('events18102020_withtypes.csv')
