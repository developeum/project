def preprocess_events_data(csv_in):
    import pandas
    import pymorphy2
    import numpy as np
    import nltk
    from nltk.corpus import stopwords
    nltk.download("stopwords")

    events_df = pandas.read_csv(csv_in)

    events_df['description'] = events_df['description'].replace(r'https?:\/\/[^\s]+', '', regex=True)
    events_df['description'] = events_df['description'].str.lower()
    events_df['description'] = events_df['description'].replace('ё', 'е', regex=True)
    events_df['description'] = events_df['description'].replace(
        r'\w*январ\w*|\w*феврал\w*|\w*март\w*|\w*апрел\w*|\w*июн\w*|\w*июл\w*|\w*август\w*|\w*сентябр\w*|\w*октябр\w*|\w*ноябр\w*|\w*декабр\w*|\bма.\b',
        ' ', regex=True)
    events_df['description'] = events_df['description'].replace(r'[^а-яА-Яa-zA-Z]', ' ', regex=True)

    events_df['name'] = events_df['name'].str.lower()
    events_df['name'] = events_df['name'].replace('ё', 'е', regex=True)
    events_df['name'] = events_df['name'].replace(
        r'\w*январ\w*|\w*феврал\w*|\w*март\w*|\w*апрел\w*|\w*июн\w*|\w*июл\w*|\w*август\w*|\w*сентябр\w*|\w*октябр\w*|\w*ноябр\w*|\w*декабр\w*|\bма.\b',
        ' ', regex=True)
    events_df['name'] = events_df['name'].replace(r'[^а-яА-Яa-zA-Z]', ' ', regex=True)

    morph = pymorphy2.MorphAnalyzer()

    stopwords = stopwords.words("russian")
    stopwords.extend(
        ['что', 'это', 'весь', 'этот', 'привет', 'так', 'вот', 'как', 'ссылка', 'регистрация', 'приглашать', 'еще',
         'год', 'спикер', 'вопрос', 'тема', 'наш', 'свой', 'время', 'который', 'выступить', 'встреча', 'мочь',
         'jenkins', 'masked', 'ваш', 'epam', 'место', 'spb'])
    descr_array = []
    names_array = []
    for i in range(len(events_df)):
        descr = events_df['description'][i]
        if not pandas.isna(descr):
            descr = [morph.parse(word)[0].normal_form for word in descr.split() if
                     morph.parse(word)[0].tag.POS not in {'INTJ', 'PRCL', 'CONJ', 'PREP', 'NPRO'}
                     and morph.parse(word)[0].normal_form not in stopwords]
            if not descr:
                descr = np.nan
            else:
                descr = ' '.join(descr)
        descr_array.append(descr)
        name = events_df['name'][i]
        if not pandas.isna(name):
            name = [morph.parse(word)[0].normal_form for word in name.split() if
                    morph.parse(word)[0].tag.POS not in {'INTJ', 'PRCL', 'CONJ', 'PREP', 'NPRO'}]
            name = ' '.join(name)
        names_array.append(name)
    events_df['name'] = names_array
    events_df['description'] = descr_array
    csv_out = 'events18102020.csv'
    events_df.to_csv(csv_out, index=False, index_label=False)


csv_in = 'meetup_tech_18102020_tz_fixed.csv'
preprocess_events_data(csv_in)
