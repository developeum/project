from flask_sqlalchemy import SQLAlchemy

from config import *

db = SQLAlchemy()

url_mask = 'postgresql://{user}:{password}@{host}:{port}/{db}'
db_url = url_mask.format(user=DB_USER, password=DB_PASS,
                         host=DB_HOST, port=DB_PORT,
                         db=DB_NAME)
