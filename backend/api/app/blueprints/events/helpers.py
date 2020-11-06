from typing import List

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
