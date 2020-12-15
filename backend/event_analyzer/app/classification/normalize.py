import nltk
import numpy as np
import pandas as pd
import pymorphy2

nltk.download("stopwords")
from langdetect import detect
from nltk.corpus import stopwords

stopwords = stopwords.words("russian")
stopwords.extend(
    ['что', 'это', 'весь', 'этот', 'привет', 'так', 'вот', 'как', 'ссылка', 'регистрация', 'приглашать', 'еще',
     'год', 'спикер', 'вопрос', 'тема', 'наш', 'свой', 'время', 'который', 'выступить', 'встреча', 'мочь',
     'jenkins', 'masked', 'ваш', 'epam', 'место', 'spb', 'новый'])

rus_names = list(pd.read_csv('static/russian_names.csv')['Name'].values)
rus_surnames = list(pd.read_csv('static/russian_surnames.csv')['Surname'].values)
for_names = list(pd.read_csv('static/foreign_names.csv')['name'].values)
all_names = rus_names + rus_surnames + for_names

pd.options.mode.chained_assignment = None

morph = pymorphy2.MorphAnalyzer()

def Normalize(events_df):
    # events_df = pd.read_json(json_in, lines=True)
    events_df['normalized_name'] = events_df['name']
    events_df['normalized_description'] = events_df['description']

    idxs = []
    for i in range(len(events_df)):
        descr = events_df['description'][i]
        name = events_df['name'][i]
        if (detect(name) != 'ru' and detect(name) != 'en') or (detect(descr) != 'ru' and detect(descr) != 'en'):
            idxs.append(i)
    events_df = events_df.drop(idxs)
    events_df.index = range(len(events_df))

    reg_exp = [
        [r'https?:\/\/[^\s]+', ''],
        ['ё', 'е'],
        [r'\w*январ\w*|\w*феврал\w*|\w*март\w*|\w*апрел\w*|\w*июн\w*|\w*июл\w*|\w*август\w*|\w*сентябр\w*|\w*октябр\w*|\w*ноябр\w*|\w*декабр\w*|\bма.\b', ' '],
        [r'[^а-яА-Яa-zA-Z]', ' ']
    ]

    events_df['normalized_description'] = events_df['normalized_description'].str.lower()
    events_df['normalized_name'] = events_df['normalized_name'].str.lower()
    for i in range(len(reg_exp)):
        events_df['normalized_description'] = events_df['normalized_description'].replace(reg_exp[i][0], reg_exp[i][1], regex=True)
        events_df['normalized_name'] = events_df['normalized_name'].replace(reg_exp[i][0], reg_exp[i][1], regex=True)

    descr_array = []
    names_array = []
    for i in range(len(events_df)):
        descr = events_df['normalized_description'][i]
        if not pd.isna(descr):
            descr = [morph.parse(word)[0].normal_form for word in descr.split() if
                     morph.parse(word)[0].tag.POS not in {'INTJ', 'PRCL', 'CONJ', 'PREP', 'NPRO'}
                     and morph.parse(word)[0].normal_form not in stopwords
                     and morph.parse(word)[0].normal_form not in all_names]
            if not descr:
                descr = np.nan
            else:
                descr = ' '.join(descr)
        descr_array.append(descr)

        name = events_df['normalized_name'][i]
        if not pd.isna(name):
            name = [morph.parse(word)[0].normal_form for word in name.split() if
                    morph.parse(word)[0].tag.POS not in {'INTJ', 'PRCL', 'CONJ', 'PREP', 'NPRO'}]
            name = ' '.join(name)
        names_array.append(name)

    events_df['normalized_name'] = names_array
    events_df['normalized_description'] = descr_array

    return events_df
    # events_df.to_json(json_out, orient='records', lines=True)
