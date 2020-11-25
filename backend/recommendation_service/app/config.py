from os import getenv
from sqlalchemy import create_engine

REDIS_HOST = getenv('REDIS_HOST')
REDIS_PORT = getenv('REDIS_PORT')

url_mask = 'postgresql://{user}:{password}@{host}:{port}/{db}'
url = url_mask.format(user=getenv('POSTGRES_USER'),
                      db=getenv('POSTGRES_DB'),
                      password=getenv('POSTGRES_PASSWORD'),
                      host=getenv('POSTGRES_HOST'),
                      port=getenv('POSTGRES_PORT'))

engine = create_engine(url)
