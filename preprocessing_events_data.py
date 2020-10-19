import pandas
import pymorphy2

events_df = pandas.read_csv('meetup_tech_18102020_tz_fixed.csv')

events_df = events_df.dropna(axis='index', how='any', subset=['description'])
events_df['description'] = events_df['description'].replace('https?:\/\/[^\s]+', '', regex=True)
events_df['description'] = events_df['description'].str.lower()
events_df['description'] = events_df['description'].replace('ё', 'е', regex=True)
events_df['description'] = events_df['description'].replace('\w*январ\w*|\w*феврал\w*|\w*март\w*|\w*апрел\w*|\w*июн\w*|\w*июл\w*|\w*август\w*|\w*сентябр\w*|\w*октябр\w*|\w*ноябр\w*|\w*декабр\w*|\w*ма.', ' ', regex=True)
events_df['description'] = events_df['description'].replace('[^а-яА-Яa-zA-Z]', ' ', regex=True)

morph = pymorphy2.MorphAnalyzer()
descr_array = []
for descr in events_df['description'].to_numpy():
    descr = [morph.parse(word)[0].normal_form for word in descr.split() if morph.parse(word)[0].tag.POS not in {'INTJ', 'PRCL', 'CONJ', 'PREP'}]
    descr_array.append(' '.join(descr))
events_df['description'] = descr_array

events_df.to_csv('events18102020.csv')
