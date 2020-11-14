import redis
import json
import numpy as np
from choose_classes_and_types import ChooseClassesAndTypes

#r = redis.Redis()

def Make_recommendation(json_in):
    user_id = json_in.get('id')
    key1 = str(user_id) + '_class'
    key2 = str(user_id) + '_type'
    classes = r.zrevrange(key1, 0,-1, withscores=True)
    types = r.zrevrange(key2, 0,-1, withscores=True)
    
    tmp_json = {'classes': {'web': None,'mobile': None,'ds': None,'qa': None,'devops': None,'busorg': None,'others_class': None},
     'types': {'hackathon': None,'webinar': None,'conference': None,'training': None,'course': None,'meetup': None,'olympiad': None,'others_type': None}}
    
    for i in range(len(classes)):
        if str(classes[i][0]) == 'b\'1\'':
            tmp_json['classes']['web'] = classes[i][1]
        elif str(classes[i][0]) == 'b\'2\'':
            tmp_json['classes']['mobile'] = classes[i][1]
        elif str(classes[i][0]) == 'b\'3\'':
            tmp_json['classes']['ds'] = classes[i][1]
        elif str(classes[i][0]) == 'b\'4\'':
            tmp_json['classes']['qa'] = classes[i][1]
        elif str(classes[i][0]) == 'b\'5\'':
            tmp_json['classes']['devops'] = classes[i][1]
        elif str(classes[i][0]) == 'b\'6\'':
            tmp_json['classes']['busorg'] = classes[i][1]
        elif str(classes[i][0]) == 'b\'7\'':
            tmp_json['classes']['others_class'] = classes[i][1]
    
    for i in range(len(types)):
        if str(types[i][0]) == 'b\'1\'':
            tmp_json['types']['others_type'] = types[i][1]
        elif str(types[i][0]) == 'b\'2\'':
            tmp_json['types']['hackathon'] = types[i][1]
        elif str(types[i][0]) == 'b\'3\'':
            tmp_json['types']['webinar'] = types[i][1]
        elif str(types[i][0]) == 'b\'4\'':
            tmp_json['types']['conference'] = types[i][1]
        elif str(types[i][0]) == 'b\'5\'':
            tmp_json['types']['training'] = types[i][1]
        elif str(types[i][0]) == 'b\'6\'':
            tmp_json['types']['course'] = types[i][1]
        elif str(types[i][0]) == 'b\'7\'':
            tmp_json['types']['meetup'] = types[i][1]
        elif str(types[i][0]) == 'b\'8\'':
            tmp_json['types']['olympiad'] = types[i][1]
                 
    json_out = ChooseClassesAndTypes(tmp_json) #json_out is a string
    return json_oun