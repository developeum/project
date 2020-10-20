import bcrypt
from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from models import User, UserStack, db

from helpers import json_validate

from .helpers import check_email

users_api = Blueprint('users_api', __name__)

@users_api.route('/register', methods=['POST'])
def register_user():
    body = request.get_json()

    good, reason = json_validate(body, {
        'email': str,
        'password': str,
        'first_name': str,
        'last_name': str,
        'stack': list
    })

    if not good:
        return {'ok': False, 'reason': reason}

    body['email'] = body['email'].lower()

    if not check_email(body['email']):
        return {'ok': False, 'reason': 'Incorrect email format'}

    if User.query.filter_by(email=body['email']).first() is not None:
        return {'ok': False, 'reason': 'Email is already registered'}

    password_hash = bcrypt.hashpw(body['password'].encode(), bcrypt.gensalt())
    new_user = User(email=body['email'],
                    password=password_hash.decode(),
                    first_name=body['first_name'],
                    last_name=body['last_name'])

    for stack_id in body['stack']:
        if not isinstance(stack_id, int):
            return {'ok': False,
                    'reason': 'Stack must be an array of integers'}

        stack = UserStack.query.filter_by(id=stack_id).first()
        if stack is None:
            return {'ok': False,
                    'reason': 'Stack with provided id doesn\'t exist'}

        new_user.stack.append(stack)

    db.session.add(new_user)
    db.session.commit()

    return {'ok': True, 'token': create_access_token(new_user)}, 200

@users_api.route('/login', methods=['POST'])
def login_user():
    body = request.get_json()

    good, reason = json_validate(body, {
        'email': str,
        'password': str
    })

    if not good:
        return {'ok': False, 'reason': reason}

    user_to_check = User.query.filter_by(email=body['email']).first()
    if user_to_check is None:
        valid = False
    else:
        valid = bcrypt.checkpw(body['password'].encode(),
                               user_to_check.password.encode())

    if not valid:
        return {'ok': False, 'reason': 'Incorrect login or password'}

    return {'ok': True, 'token': create_access_token(user_to_check)}
