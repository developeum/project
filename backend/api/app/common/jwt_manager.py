from flask_jwt_extended import JWTManager

from .models import User

jwt = JWTManager()


@jwt.user_identity_loader
def custom_identity_loader(user):
    return user.id


@jwt.user_loader_callback_loader
def custom_user_loader(identity):
    return User.query.filter_by(id=identity).first()


@jwt.expired_token_loader
def expired_token_handler(token):
    return {'ok': False, 'reason': 'Token has expired'}, 403


@jwt.invalid_token_loader
def invalid_token_handler(token):
    return {'ok': False, 'reason': 'Token is invalid'}, 403


@jwt.unauthorized_loader
def no_token_handler(token):
    return {'ok': False, 'reason': 'No access token provided'}, 403
