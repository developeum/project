from typing import Any, Dict

def json_validate(body: Any, required: Dict[str, type]):
    ONLY_JSON = 'Request body must be a json object'
    KEY_NOT_PROVIDED = 'Required key is not provided: %s'
    INCORRECT_TYPE = 'Incorrect key type: %s'

    if not isinstance(body, dict):
        return False, ONLY_JSON

    for field, field_type in required.items():
        if field not in body:
            return False, KEY_NOT_PROVIDED % field

        if not isinstance(body[field], field_type):
            return False, INCORRECT_TYPE % field

    return True, None
