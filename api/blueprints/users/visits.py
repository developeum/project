from datetime import datetime

from common.helpers import accepts_json
from common.models import Event, UserVisit, db
from flask import request
from flask_jwt_extended import current_user, jwt_required

from .messages import *

@jwt_required
@accepts_json(
    event_id=(True, int)
)
def add_visited_page():
    body = request.get_json()

    event = Event.query.filter_by(id=body['event_id']).first()
    if event is None:
        return INCORRECT_EVENT_ID, 200

    visit = UserVisit.query.filter_by(user=current_user, event=event).first()
    if visit is None:
        visit = UserVisit(event, current_user, datetime.utcnow())
        db.session.add(visit)
    else:
        visit.visit_time = datetime.utcnow()

    db.session.commit()

    return {'ok': True}, 200

@jwt_required
def get_visited_pages():
    skip = request.args.get('skip', '0')
    limit = request.args.get('limit', '20')

    if not skip.isdigit():
        return {'ok': False, 'reason': 'skip parameter isn\'t integer'}, 200
    if not limit.isdigit():
        return {'ok': False, 'reason': 'limit parameter isn\'t integer'}, 200

    skip, limit = int(skip), int(limit)

    visited = current_user.visited[skip:skip+limit]

    return {
        'ok': True,
        'events': [
            {
                'id': event.id,
                'name': event.name,
                'type': {
                    'id': event.event_type.id,
                    'name': event.event_type.event_type
                }
            } for event in visited
        ]
    }, 200
