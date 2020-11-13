import redis

#r = redis.Redis()

def Update_user(json_in):
    user_id = json_in.get('id')
    categories = json_in.get('event').get('categories')
    types = json_in.get('event').get('event_type')
    key1 = str(user_id) + '_class'
    key2 = str(user_id) + '_type'
    r.zincrby(key1, 2, categories[0])
    r.zincrby(key2, 2, types)