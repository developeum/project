from os import getenv

DB_HOST = 'postgres'
DB_PORT = 5432

DB_NAME = getenv('POSTGRES_DB')
DB_USER = getenv('POSTGRES_USER')
DB_PASS = getenv('POSTGRES_PASSWORD')

SECRET_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'bmp', 'gif'}
STATIC_DIR = '/'
UPLOAD_DIR = '/static/'
