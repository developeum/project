from functools import wraps

from flask import request

def accepts_json(**fields):
    def decorator(func):
        ONLY_JSON = 'Request body must be a json object'
        KEY_NOT_PROVIDED = 'Required key is not provided: %s'
        INCORRECT_TYPE = 'Incorrect key type: %s'

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
