import redis
import json
import numpy as np

#r = redis.Redis() 

def Create_user_set (user_id):
    key1 = str(user_id) + '_class'
    key2 = str(user_id) + '_type'
    r.zadd(key1, {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0})
    r.zadd(key2, {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 1: 0})

def Update_user_set(user_id, stack):
    key1 = str(user_id) + '_class'
    r.zincrby(key1, 10, stack[0])

def Trigger_it_when_registrate_user(json_in):
    user_id = json_in.get('id')
    Create_user_set(user_id)
    stack = json_in.get('stack')
    if stack != np.nan:
        Update_user_set(user_id, stack)
