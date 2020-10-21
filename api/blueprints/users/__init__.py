from flask import Blueprint

from .auth import login_user, register_user
from .profile import get_profile_info, update_profile_info

users_api = Blueprint('users_api', __name__)

users_api.add_url_rule('/register', 'register', register_user,
                       methods=['POST'])
users_api.add_url_rule('/login', 'login', login_user,
                       methods=['POST'])

users_api.add_url_rule('/me', 'get_info', get_profile_info,
                       methods=['GET'])
users_api.add_url_rule('/me', 'update_info', update_profile_info,
                       methods=['POST'])
