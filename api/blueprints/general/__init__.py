from common.models import (
    City, EventCategory, EventType,
    UserStack, UserStatus
)
from flask import Blueprint, request, jsonify

general_api = Blueprint('general_api', __name__)

@general_api.route('/cities')
def get_city_list():
    skip = request.args.get('skip', 0, type=int)
    limit = request.args.get('limit', 10, type=int)

    cities = City.query.offset(skip).limit(limit).all()

    return jsonify([
        city.as_json() for city in cities
    ]), 200

@general_api.route('/statuses')
def get_status_list():
    statuses = UserStatus.query.all()

    return jsonify([
        status.as_json() for status in statuses
    ]), 200

@general_api.route('/stacks')
def get_stack_list():
    stacks = UserStack.query.all()

    return jsonify([
        stack.as_json() for stack in stacks
    ]), 200

@general_api.route('/categories')
def get_category_list():
    categories = EventCategory.query.all()

    return jsonify([
        category.as_json() for category in categories
    ]), 200

@general_api.route('/event_types')
def get_event_type_list():
    event_types = EventType.query.all()

    return jsonify([
        event_type.as_json() for event_type in event_types
    ]), 200
