from os import getenv

DB_NAME = getenv('POSTGRES_DB')
DB_USER = getenv('POSTGRES_USER')
DB_PASS = getenv('POSTGRES_PASSWORD')
DB_HOST = getenv('POSTGRES_HOST')
DB_PORT = getenv('POSTGRES_PORT')
