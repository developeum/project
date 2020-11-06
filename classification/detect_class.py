import pandas as pd
import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

def Detect_class(csv_in, csv_out):
    
    pd.options.mode.chained_assignment = None

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
    final_df = final_df.drop(['normalized_name'],axis=1)
    final_df = final_df.drop(['normalized_description'],axis=1)

    final_df.to_csv(csv_out, index=False, index_label=False)


Final_function('events_crawlers_02112020.csv', 'Ff_events_crawlers_02112020.csv')
