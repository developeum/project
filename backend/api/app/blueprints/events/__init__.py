from datetime import datetime

from common.helpers import parse_int_array, project, rpc_cluster
from common.models import Event, EventCategoryLink
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_optional

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
@jwt_optional
def get_event_list():
    current_user = get_jwt_identity()

    skip = request.args.get('skip', 0, type=int)
    limit = request.args.get('limit', 20, type=int)

    types = parse_int_array(request.args.get('type', ''))
    categories = parse_int_array(request.args.get('category', ''))
    cities = parse_int_array(request.args.get('city', ''))

    starts_at_min = request.args.get('starts_at_min', '')
    starts_at_max = request.args.get('starts_at_max', '')

    name = request.args.get('name', '')

    # TODO: enable and test recommendation service here
    # if current_user is None:
    if True:
        events_query = Event.query
    else:
        events_query = rpc_cluster.recommendation_service.get_recommendations({
            'user_id': current_user.id
        })

    date_format = '%Y-%m-%d'

    if name != '':
        events_query = events_query.filter(
            Event.name.ilike('%{}%'.format(name))
        )

    if starts_at_min != '':
        try:
            starts_at_min = datetime.strptime(starts_at_min, date_format)
            events_query = events_query.filter(
                Event.event_time >= starts_at_min
            )
        except:
            return {'ok': False,
                    'reason': 'Incorrect starts_at_min parameter'}

    if starts_at_max != '':
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

    default_keys = 'id,name,event_type,event_time'
    fields = request.args.get('fields', default_keys).split(',')

    return jsonify([
        project(event.as_json(), fields) for event in events
    ]), 200
