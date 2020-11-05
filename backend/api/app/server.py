from os import urandom

from flask import Flask

from blueprints.events import events_api
from blueprints.general import general_api
from blueprints.users import users_api
from common.database import db, db_url
from common.jwt_manager import jwt
from config import SECRET_KEY

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['JWT_SECRET_KEY'] = SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 7 * 86400
app.config['JWT_HEADER_NAME'] = 'X-Session-Token'
app.config['JWT_HEADER_TYPE'] = ''

db.init_app(app)
jwt.init_app(app)

app.register_blueprint(users_api, url_prefix='/api/user')
app.register_blueprint(general_api, url_prefix='/api/general')
app.register_blueprint(events_api, url_prefix='/api/events')

if __name__ == '__main__':
    app.run(port=8000)
