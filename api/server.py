from os import urandom

from flask import Flask

from blueprints.events import events_api
from blueprints.general import general_api
from blueprints.users import users_api
from common.database import db, db_url
from common.jwt_manager import jwt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['JWT_SECRET_KEY'] = urandom(32)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 7 * 86400
app.config['JWT_HEADER_NAME'] = 'X-Session-Token'
app.config['JWT_HEADER_TYPE'] = ''

db.init_app(app)
jwt.init_app(app)

app.register_blueprint(users_api, url_prefix='/api/user')
app.register_blueprint(general_api, url_prefix='/api/general')
app.register_blueprint(events_api, url_prefix='/api/events')

@app.after_request
def after_request_func(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Request-Headers'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    return response

if __name__ == '__main__':
    app.run(port=8000)
