from common.helpers import accepts_json
from common.models import City, UserStack, UserStatus, db
from flask import request
from flask_jwt_extended import current_user, jwt_required

from .messages import *

@jwt_required
def get_profile_info():
    return current_user.as_json(), 200

@jwt_required
@accepts_json(
    phone=(False, str),
    first_name=(False, str),
    last_name=(False, str),
    status=(False, int),
    city=(False, int),
    stack=(False, [int])
)
def update_profile_info():
    body = request.get_json()

    profile_fields = [
        'phone',
        'first_name',
        'last_name',
        'status',
        'city',
        'stack'
    ]

    for field in profile_fields:
        if field not in body:
            continue

        if field == 'status':
            new_status = UserStatus.query.filter_by(id=body['status']).first()

            if new_status is None:
                return INCORRECT_STATUS_ID, 200

            current_user.status = new_status
        elif field == 'city':
            new_city = City.query.filter_by(id=body['status']).first()

            if new_city is None:
                return INCORRECT_CITY_ID, 200

            current_user.city = new_city
        elif field == 'stack':
            for stack_id in body['stack']:
                stack = UserStack.query.filter_by(id=stack_id).first()

                if stack is None:
                    return INCORRECT_STACK_ID, 200

                current_user.stack.append(stack)
        else:
            setattr(current_user, field, body[field])

    db.session.commit()

    return {'ok': True}, 200
