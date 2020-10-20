from os import urandom

from flask import Flask

from database import db, db_url
from jwt_manager import jwt
from users.routes import users_api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['JWT_SECRET_KEY'] = urandom(32)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 7 * 86400

db.init_app(app)
jwt.init_app(app)

app.register_blueprint(users_api, url_prefix='/api/user')

if __name__ == '__main__':
    app.run()
