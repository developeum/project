from common.helpers import accepts_json, dispatch
from common.models import City, EventCategory, UserStatus, db
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
            new_city = City.query.filter_by(id=body['city']).first()

            if new_city is None:
                return INCORRECT_CITY_ID, 200

            current_user.city = new_city
        elif field == 'stack':
            if current_user.stack == body['stack']:
                continue

            old_stack = [category.id for category in current_user.stack]
            current_user.stack = []

            for category_id in body['stack']:
                category = (EventCategory.query.filter_by(id=category_id)
                                               .first())

                if category is None:
                    return INCORRECT_CATEGORY_ID, 200

                current_user.stack.append(category)

            new_stack = [category.id for category in current_user.stack]

            dispatch('user_stack_changed', {
                'user_id': current_user.id,
                'old_stack': old_stack,
                'new_stack': new_stack
            })
        else:
            setattr(current_user, field, body[field])

    db.session.commit()

    return {'ok': True}, 200
