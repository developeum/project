from os.path import normpath
from uuid import uuid4

from common.models import db
from config import ALLOWED_EXTENSIONS, STATIC_DIR, UPLOAD_DIR
from flask import request
from flask_jwt_extended import current_user, jwt_required

from .helpers import get_file_extension
from .messages import *

@jwt_required
def upload_avatar():
    avatar = request.files.get('avatar', None)
    if avatar is None:
        return NO_FILE_PROVIDED, 200

    extension = get_file_extension(avatar.filename)
    if extension not in ALLOWED_EXTENSIONS:
        return EXTENSION_NOT_ALLOWED, 200

    filename = '{base}.{extension}'.format(base=uuid4(), extension=extension)

    relative_path = (UPLOAD_DIR + '/' + filename).replace('//', '/')
    absolute_path = normpath(STATIC_DIR + '/' + relative_path)

    current_user.profile_img = relative_path

    avatar.save(absolute_path)
    db.session.commit()

    return {'ok': True, 'avatar': relative_path}

@jwt_required
def get_avatar_path():
    return {'ok': True, 'avatar': current_user.profile_img}
