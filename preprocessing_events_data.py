def preprocess_events_data(csv_in, csv_out):
    import pandas
    import pymorphy2
    import numpy as np
    import nltk
    from nltk.corpus import stopwords
    nltk.download("stopwords")

    events_df = pandas.read_csv(csv_in)
    events_df['normalized_name'] = events_df['name']
    events_df['normalized_description'] = events_df['description']

    events_df['normalized_description'] = events_df['normalized_description'].replace(r'https?:\/\/[^\s]+', '', regex=True)
    events_df['normalized_description'] = events_df['normalized_description'].str.lower()
    events_df['normalized_description'] = events_df['normalized_description'].replace('ё', 'е', regex=True)
    events_df['normalized_description'] = events_df['normalized_description'].replace(
        r'\w*январ\w*|\w*феврал\w*|\w*март\w*|\w*апрел\w*|\w*июн\w*|\w*июл\w*|\w*август\w*|\w*сентябр\w*|\w*октябр\w*|\w*ноябр\w*|\w*декабр\w*|\bма.\b',
        ' ', regex=True)
    events_df['normalized_description'] = events_df['normalized_description'].replace(r'[^а-яА-Яa-zA-Z]', ' ', regex=True)

    events_df['normalized_name'] = events_df['normalized_name'].str.lower()
    events_df['normalized_name'] = events_df['normalized_name'].replace('ё', 'е', regex=True)
    events_df['normalized_name'] = events_df['normalized_name'].replace(
        r'\w*январ\w*|\w*феврал\w*|\w*март\w*|\w*апрел\w*|\w*июн\w*|\w*июл\w*|\w*август\w*|\w*сентябр\w*|\w*октябр\w*|\w*ноябр\w*|\w*декабр\w*|\bма.\b',
        ' ', regex=True)
    events_df['normalized_name'] = events_df['normalized_name'].replace(r'[^а-яА-Яa-zA-Z]', ' ', regex=True)

    morph = pymorphy2.MorphAnalyzer()
    stopwords = stopwords.words("russian")
    stopwords.extend(
        ['что', 'это', 'весь', 'этот', 'привет', 'так', 'вот', 'как', 'ссылка', 'регистрация', 'приглашать', 'еще',
         'год', 'спикер', 'вопрос', 'тема', 'наш', 'свой', 'время', 'который', 'выступить', 'встреча', 'мочь',
         'jenkins', 'masked', 'ваш', 'epam', 'место', 'spb', 'новый'])

    rus_names = list(pandas.read_csv('russian_names.csv')['Name'].values)
    rus_surnames = list(pandas.read_csv('russian_surnames.csv')['Surname'].values)
    for_names = list(pandas.read_csv('foreign_names.csv')['name'].values)
    all_names = rus_names + rus_surnames + for_names

    descr_array = []
    names_array = []
    for i in range(len(events_df)):
        descr = events_df['normalized_description'][i]
        if not pandas.isna(descr):
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
        if not pandas.isna(name):
            name = [morph.parse(word)[0].normal_form for word in name.split() if
                    morph.parse(word)[0].tag.POS not in {'INTJ', 'PRCL', 'CONJ', 'PREP', 'NPRO'}]
            name = ' '.join(name)
        names_array.append(name)

    events_df['normalized_name'] = names_array
    events_df['normalized_description'] = descr_array
    events_df = events_df[['name', 'normalized_name', 'event_time', 'description', 'normalized_description', 'city', 'category']]

    events_df.to_csv(csv_out, index=False, index_label=False)


csv_in = 'meetup_tech_18102020_tz_fixed.csv'
csv_out = 'events18102020.csv'
preprocess_events_data(csv_in, csv_out)
