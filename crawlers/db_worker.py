from config import (
    DB_NAME, DB_HOST, DB_USER,
    DB_PASS, DB_PORT
)
from datetime import datetime
import psycopg2

connection = psycopg2.connect(
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT
)

cursor = connection.cursor()
city_ids = dict()

def add_event(event_time: datetime,
              city: str,
              description: str,
              place: str,
              logo_path: str):
    """ Add event to database, but do not commit changes """

    if city in city_ids.keys():
        city_id = city_ids[city]
    else:
        cursor.execute("SELECT id FROM cities WHERE city=%s", (city,))
        entry = cursor.fetchone()

        if entry is None:
            cursor.execute("INSERT INTO cities(city) VALUES (%s) RETURNING id",
                           (city,))
            entry = cursor.fetchone()

        city_id = city_ids[city] = entry[0]

    cursor.execute("INSERT INTO events(event_time, city, description, "\
                   "place, logo_path) VALUES (%s, %s, %s, %s, %s)",
                   (event_time, city_id, description, place, logo_path))

def commit_changes():
    """ Commit changes to database """
    connection.commit()
