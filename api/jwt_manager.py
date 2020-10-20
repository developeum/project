from flask_jwt_extended import JWTManager
from models import User

jwt = JWTManager()

@jwt.user_identity_loader
def custom_identity_loader(user):
    return user.id

@jwt.user_loader_callback_loader
def custom_user_loader(identity):
    return User.query.filter_by(id=identity).first()
