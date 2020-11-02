def Final_function(csv_in, csv_out):
    import pandas as pd
    import pymorphy2
    import numpy as np
    import nltk
    from nltk.corpus import stopwords
    nltk.download("stopwords")
    from langdetect import detect

    pd.options.mode.chained_assignment = None

    import pickle
    from sklearn.feature_extraction.text import TfidfVectorizer

    # the first function

    events_df = pd.read_csv(csv_in)
    events_df['normalized_name'] = events_df['name']
    events_df['normalized_description'] = events_df['description']

    idxs = []
    for i in range(len(events_df)):
        descr = events_df['description'][i]
        name = events_df['name'][i]
        if (detect(name) != 'ru' and detect(name) != 'en') or (detect(descr) != 'ru' and detect(descr) != 'en'):
            idxs.append(i)
    events_df = events_df.drop(idxs)
    events_df = events_df.reindex(range(0, len(events_df)))

    events_df['normalized_description'] = events_df['normalized_description'].replace(r'https?:\/\/[^\s]+', '',
                                                                                      regex=True)
    events_df['normalized_description'] = events_df['normalized_description'].str.lower()
    events_df['normalized_description'] = events_df['normalized_description'].replace('ё', 'е', regex=True)
    events_df['normalized_description'] = events_df['normalized_description'].replace(
        r'\w*январ\w*|\w*феврал\w*|\w*март\w*|\w*апрел\w*|\w*июн\w*|\w*июл\w*|\w*август\w*|\w*сентябр\w*|\w*октябр\w*|\w*ноябр\w*|\w*декабр\w*|\bма.\b',
        ' ', regex=True)
    events_df['normalized_description'] = events_df['normalized_description'].replace(r'[^а-яА-Яa-zA-Z]', ' ',
                                                                                      regex=True)

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

    rus_names = list(pd.read_csv('russian_names.csv')['Name'].values)
    rus_surnames = list(pd.read_csv('russian_surnames.csv')['Surname'].values)
    for_names = list(pd.read_csv('foreign_names.csv')['name'].values)
    all_names = rus_names + rus_surnames + for_names

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
    events_df = events_df[
        ['name', 'normalized_name', 'event_type', 'event_time', 'description', 'normalized_description', 'city',
         'categories']]
    
    # the second function

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

    # the third function

    clas = []
    ds = ['AI', 'Data Science', 'ai', 'data science', 'data engineering', 'data scientist', 'deep learning',
          'машинное обучение', 'нейросети']
    mobile = ['Android', 'mobile']
    qa = ['QA', 'qa', 'тестировщик']
    web = ['Web', 'Front-end', 'frontend', 'фронтенд-разработчик']
    devops = ['DevOps', 'devops']
    busorg = ['BA', 'Business', 'HR', 'Marketing', 'hr', 'project manager', 'менеджмент']

    possible_class = ['ds', 'mobile', 'qa', 'web', 'devops', 'busorg']

    categories = events_df['categories'].to_numpy().astype(str)

    for x in categories:
        count = []
        mask = np.isin(x.split(','), ds)
        count.append(np.count_nonzero(mask == bool("True")))

        mask = np.isin(x.split(','), mobile)
        count.append(np.count_nonzero(mask == bool("True")))

        mask = np.isin(x.split(','), qa)
        count.append(np.count_nonzero(mask == bool("True")))

        mask = np.isin(x.split(','), web)
        count.append(np.count_nonzero(mask == bool("True")))

        mask = np.isin(x.split(','), devops)
        count.append(np.count_nonzero(mask == bool("True")))

        mask = np.isin(x.split(','), busorg)
        count.append(np.count_nonzero(mask == bool("True")))

        if np.count_nonzero(count) > 0:
            ind = np.argmax(count)
            clas.append(possible_class[ind])
        else:
            clas.append('undefined')

    cl = pd.DataFrame(clas, columns=['class_tmp'])

    temp_df = events_df.join(cl, how='inner')

    pkl_filename = "pickle_model_ada.pkl"
    with open(pkl_filename, 'rb') as file:
        pickle_model = pickle.load(file)

    pkl_vec_filename = "pickle_vect.pkl"
    with open(pkl_vec_filename, 'rb') as file:
        pickle_vec = pickle.load(file)

    np.set_printoptions(precision=3, suppress=True)

    label = temp_df['class_tmp'].to_numpy()
    desc = temp_df['normalized_description'].to_numpy()

    description = pickle_vec.transform(desc)

    class1 = []

    i = 0
    for x in label:
        if x == 'busorg':
            class1.append('busorg')
        elif x == 'devops':
            class1.append('devops')
        elif x == 'ds':
            class1.append('ds')
        elif x == 'mobile':
            class1.append('mobile')
        elif x == 'qa':
            class1.append('qa')
        elif x == 'web':
            class1.append('web')
        else:
            proba = pickle_model.predict_proba(description[i])
            proba = proba * 100
            print(proba)
            if max(proba[0] > 49.9):
                print(np.argmax(proba[0]))
                if np.argmax(proba[0]) == 0:
                    class1.append('busorg')
                elif np.argmax(proba[0]) == 1:
                    class1.append('devops')
                elif np.argmax(proba[0]) == 2:
                    class1.append('ds')
                elif np.argmax(proba[0]) == 3:
                    class1.append('mobile')
                elif np.argmax(proba[0]) == 4:
                    class1.append('qa')
                elif np.argmax(proba[0]) == 5:
                    class1.append('web')
                else:
                    class1.append('other')
            else:
                class1.append('other')

        i = i + 1

    new_class = pd.DataFrame(class1, columns=['class'])
    final_df = temp_df.join(new_class, how='inner')
    final_df = final_df.drop(['class_tmp'], axis=1)

    final_df.to_csv(csv_out, index=False, index_label=False)


Final_function('events_crawlers_02112020.csv', 'Ff_events_crawlers_02112020.csv')
