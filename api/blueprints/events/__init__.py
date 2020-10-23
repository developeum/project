from datetime import datetime

from common.models import Event, EventCategoryLink
from flask import Blueprint, request

from .helpers import project

events_api = Blueprint('events_api', __name__)

@events_api.route('/<int:event_id>')
def get_event_info(event_id: int):
    event = Event.query.filter_by(id=event_id).first()

    if event is None:
        return {'ok': False,
                'reason': 'Event with provided id doesn\'t exist'}, 200

    return {
        'ok': True,
        'event': event.as_json()
    }, 200

@events_api.route('')
def get_event_list():
    skip = request.args.get('skip', 0, type=int)
    limit = request.args.get('limit', 20, type=int)

    types = request.args.getlist('type', type=int)
    categories = request.args.getlist('category', type=int)
    cities = request.args.getlist('city', type=int)

    starts_at_min = request.args.get('starts_at_min')
    starts_at_max = request.args.get('starts_at_max')

    name = request.args.get('name')

    events_query = Event.query

    date_format = '%Y-%m-%d'

    if name is not None:
        events_query = events_query.filter(
            Event.name.ilike('%{}%'.format(name))
        )

    if starts_at_min is not None:
        try:
            starts_at_min = datetime.strptime(starts_at_min, date_format)
            events_query = events_query.filter(
                Event.event_time >= starts_at_min
            )
        except:
            return {'ok': False,
                    'reason': 'Incorrect starts_at_min parameter'}

    if starts_at_max is not None:
        try:
            starts_at_max = datetime.strptime(starts_at_max, date_format)
            events_query = events_query.filter(
                Event.event_time <= starts_at_max
            )
        except:
            return {'ok': False,
                    'reason': 'Incorrect starts_at_max parameter'}

    # As soon as event <-> category is many-to-many relationship
    # We have to filter them using intermediate table
    if categories != []:
        events_query = events_query.distinct().join(
            EventCategoryLink, Event.id == EventCategoryLink.event_id
        ).filter(EventCategoryLink.category_id.in_(categories))

    if types != []:
        events_query = events_query.filter(Event.event_type_id.in_(types))
    if cities != []:
        events_query = events_query.filter(Event.city_id.in_(cities))

    events = events_query[skip:skip+limit]

    fields = request.args.get('fields', 'id,name,event_type,event_time').split(',')

    return {
        'ok': True,
        'events': [
            project(event.as_json(), fields) for event in events
        ]
    }, 200
