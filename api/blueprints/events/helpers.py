from typing import List

def project(dict_obj: dict, fields: List[str]) -> dict:
    return {
        field: dict_obj.get(field, 'no such field')
        for field in fields
    }
