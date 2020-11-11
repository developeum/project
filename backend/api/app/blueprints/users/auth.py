from common.helpers import accepts_json
from common.models import EventCategory, User, db
from flask import request
from flask_jwt_extended import create_access_token, current_user, jwt_required

from .helpers import (check_password, hash_password, is_email_correct,
                      is_email_registered)
from .messages import *

@accepts_json(
    email=(True, str),
    password=(True, str),
    first_name=(True, str),
    last_name=(True, str),
    stack=(True, [int])
)
def register_user():
    body = request.get_json()

    body['email'] = body['email'].lower()

    if not is_email_correct(body['email']):
        return INCORRECT_EMAIL_FORMAT, 200

    if is_email_registered(body['email']):
        return EMAIL_REGISTERED, 200

    new_user = User(email=body['email'],
                    password=hash_password(body['password']),
                    first_name=body['first_name'],
                    last_name=body['last_name'])

    for category_id in body['stack']:
        category = EventCategory.query.filter_by(id=category_id).first()

        if category is None:
            return INCORRECT_CATEGORY_ID, 200

        new_user.stack.append(category)

    db.session.add(new_user)
    db.session.commit()

    return create_access_token(new_user), 200

@accepts_json(
    email=(True, str),
    password=(True, str)
)
def login_user():
    body = request.get_json()

    user_to_check = User.query.filter_by(email=body['email']).first()

    if user_to_check is None:
        valid = False
    else:
        valid = check_password(user_to_check, body['password'])

    if not valid:
        return INCORRECT_CREDENTIALS, 200

    return create_access_token(user_to_check), 200

@jwt_required
@accepts_json(
    old_password=(True, str),
    email=(False, str),
    password=(False, str)
)
def update_credentials():
    body = request.get_json()

    email = body.get('email', current_user.email).lower()
    password = body.get('password', '')

    if check_password(current_user, body['old_password']):
        if current_user.email != email:
            if not is_email_correct(email):
                return INCORRECT_EMAIL_FORMAT, 200

            if is_email_registered(email):
                return EMAIL_REGISTERED, 200

            current_user.email = email

        if password != '':
            current_user.password = hash_password(password)

        db.session.commit()

        return {'ok': True}, 200
    else:
        return INCORRECT_CREDENTIALS, 200
