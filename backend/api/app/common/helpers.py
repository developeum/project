from functools import wraps
from typing import List

from config import RABBITMQ_HOST, RABBITMQ_PASS, RABBITMQ_USER
from flask import request
from nameko.standalone.events import event_dispatcher

ONLY_JSON = 'Request body must be a json object'
KEY_NOT_PROVIDED = 'Required key is not provided: %s'
INCORRECT_TYPE = 'Incorrect key type: %s'

_dispatch = event_dispatcher({
    'AMQP_URI': 'pyamqp://{user}:{password}@{host}'.format(
        user=RABBITMQ_USER,
        password=RABBITMQ_PASS,
        host=RABBITMQ_HOST
    )
})


def accepts_json(**fields):
    def decorator(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            body = request.get_json()

            if not isinstance(body, dict):
                return {'ok': False, 'reason': ONLY_JSON}, 200

            for key, (required, key_type) in fields.items():
                if key not in body:
                    if required:
                        return {'ok': False,
                                'reason': KEY_NOT_PROVIDED % key}, 200
                    else:
                        continue
                else:
                    valid = True

                    if isinstance(key_type, type):
                        if not isinstance(body[key], key_type):
                            valid = False
                    elif isinstance(key_type, list):
                        if not isinstance(body[key], list):
                            valid = False

                        if not all(isinstance(item, key_type[0])
                                   for item in body[key]):
                            valid = False

                    if not valid:
                        return {'ok': False,
                                'reason': INCORRECT_TYPE % key}, 200

            return func(*args, **kwargs)
        return decorated
    return decorator


def project(dict_obj: dict, fields: List[str]) -> dict:
    return {
        field: dict_obj.get(field, 'no such field')
        for field in fields
    }


def parse_int_array(as_str: str) -> List[int]:
    splitted = as_str.split(',')

    return [
        int(elem) for elem in splitted if elem.isdigit()
    ]


def dispatch(type: str, payload: str) -> None:
    _dispatch('api', type, payload)
