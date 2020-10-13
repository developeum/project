from config import (
    DB_NAME, DB_HOST, DB_USER,
    DB_PASS, DB_PORT
)
from .sanitizers import sanitize
from datetime import datetime
from typing import List
import psycopg2

connection = psycopg2.connect(
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT
)

cursor = connection.cursor()
table_cache = dict()

def select_or_insert(table: str, column: str, value: str):
    """ 
        Find entry in list-like table if provided value exists in that table
        Create new one if it doesn't
    """

    select_query = 'SELECT id FROM {} '\
                   'WHERE {}=%s'.format(table, column)
    insert_query = 'INSERT INTO {} ({}) '\
                   'VALUES (%s) RETURNING id'.format(table, column)

    if table not in table_cache:
        table_cache[table] = dict()

    id_cache = table_cache[table]

    if value in id_cache:
        return id_cache[value]
    else:
        cursor.execute(select_query, (value,))
        entry = cursor.fetchone()

        if entry is None:
            cursor.execute(insert_query, (value,))
            entry = cursor.fetchone()

        id_cache[value] = entry[0]
        return entry[0]

def store_event(name: str, event_time: datetime, city: str, place: str,
                source_url: str, description: str,
                categories: List[str] = [],
                logo_path: str = None):
    """
        Add event to database, but do not commit changes
    """

    event_insert_query = 'INSERT INTO events (name, event_time, city, '\
                         'place, source_url, description, logo_path) '\
                         'VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id'
    links_insert_query = 'INSERT INTO event_category_links (event_id, '\
                         'category_id) VALUES (%s, %s)'

    name = sanitize(name)
    place = sanitize(place)
    description = sanitize(description)

    city_id = select_or_insert('cities', 'city', city)

    cursor.execute(event_insert_query, (name, event_time, city_id, place, 
                                        source_url, description, logo_path))
    event_id = cursor.fetchone()[0]

    for category in categories:
        category_id = select_or_insert('categories', 'category', category)
        cursor.execute(links_insert_query, (event_id, category_id))

def commit_changes():
    """
        Commit changes to database
    """

    connection.commit()
