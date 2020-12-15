from os import getenv

DB_NAME = getenv('POSTGRES_DB')
DB_USER = getenv('POSTGRES_USER')
DB_PASS = getenv('POSTGRES_PASSWORD')
DB_HOST = getenv('POSTGRES_HOST')
DB_PORT = getenv('POSTGRES_PORT')

RABBITMQ_HOST = getenv('RABBITMQ_HOST')
RABBITMQ_USER = getenv('RABBITMQ_DEFAULT_USER')
RABBITMQ_PASS = getenv('RABBITMQ_DEFAULT_PASS')

SECRET_KEY = getenv('JWT_SECRET_KEY')

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'bmp', 'gif'}
STATIC_DIR = '/'
UPLOAD_DIR = '/static/'
