from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

mask = 'postgresql://{user}:{password}@{host}:{port}/{db}'
db_url = mask.format(user=DB_USER, password=DB_PASS,
                     host=DB_HOST, port=DB_PORT,
                     db=DB_NAME)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
db = SQLAlchemy(app)

from models import *
