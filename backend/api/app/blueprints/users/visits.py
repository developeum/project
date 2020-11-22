from datetime import datetime

from common.helpers import accepts_json, project, dispatch
from common.models import Event, UserVisit, VisitTypeEnum, db
from flask import jsonify, request
from flask_jwt_extended import current_user, jwt_required

from .messages import *


@jwt_required
@accepts_json(
    event_id=(True, int),
    type=(False, str)
)
def add_visited_page():
    body = request.get_json()

    visit_type = body.get('type', 'external')
    visit_type = {
        'internal': VisitTypeEnum.internal,
        'external': VisitTypeEnum.external
    }.get(visit_type, None)

    if visit_type is None:
        return INCORRECT_VISIT_TYPE, 200

    event = Event.query.filter_by(id=body['event_id']).first()
    if event is None:
        return INCORRECT_EVENT_ID, 200

    visit = UserVisit.query.filter_by(user=current_user,
                                      event=event,
                                      visit_type=visit_type).first()
    now = datetime.utcnow()

    if visit is None:
        visit = UserVisit(event, current_user, now, visit_type)
        db.session.add(visit)
    else:
        visit.visit_time = now

    dispatch('event_visited', {
        'user_id': current_user.id,
        'event_id': event.id,
        'visit_type': body.get('type', 'external'),
        'categories': [category.id for category in event.categories],
        'event_type': event.event_type_id
    })

    db.session.commit()

    return {'ok': True}, 200


@jwt_required
def get_visited_pages():
    skip = request.args.get('skip', 0, type=int)
    limit = request.args.get('limit', 20, type=int)

    visited = current_user.visited[skip:skip+limit]

    keys = ['id', 'name', 'event_type']

    return jsonify([
        project(event.as_json(), keys) for event in visited
    ]), 200
