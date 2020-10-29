from flask import Blueprint

from .auth import login_user, register_user, update_credentials
from .profile import get_profile_info, update_profile_info
from .visits import add_visited_page, get_visited_pages
from .avatar import upload_avatar, get_avatar_path

users_api = Blueprint('users_api', __name__)

users_api.add_url_rule('/register', 'register',
                       register_user, methods=['POST'])
users_api.add_url_rule('/login', 'login',
                       login_user, methods=['POST'])
users_api.add_url_rule('/me/credentials', 'credentials',
                       update_credentials, methods=['POST'])

users_api.add_url_rule('/me', 'get_info',
                       get_profile_info, methods=['GET'])
users_api.add_url_rule('/me', 'update_info',
                       update_profile_info, methods=['POST'])

users_api.add_url_rule('/me/visited', 'add_visited_page',
                       add_visited_page, methods=['POST'])
users_api.add_url_rule('/me/visited', 'get_visited_pages',
                       get_visited_pages, methods=['GET'])

users_api.add_url_rule('/me/avatar', 'upload_avatar',
                       upload_avatar, methods=['POST'])
users_api.add_url_rule('/me/avatar', 'get_avatar_path',
                       get_avatar_path, methods=['GET'])
