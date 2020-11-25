from datetime import datetime
from typing import Dict

from nameko.events import event_handler
from nameko.rpc import rpc
from redis import Redis
from sqlalchemy.orm import scoped_session, sessionmaker

from config import REDIS_HOST, REDIS_PORT, engine
from models import Event, EventCategory

factory = sessionmaker(bind=engine)
Session = scoped_session(factory)


class RecommendationService:
    name = 'recommendation_service'

    # Redis configuration
    _redis = Redis(host=REDIS_HOST, port=REDIS_PORT)
    _key_format = 'user:{id}:{name}'

    # Key ranges
    _event_category_range = range(1, 8)
    _event_type_range = range(1, 9)

    # Awards
    _award_for_registration = 10
    _award_for_visit = {
        'internal': 1,
        'external': 2
    }

    def _dump_interest_vector(self, user_id: int,
                              vector_name: str,
                              vector: Dict[int, int]) -> None:
        """
            Save user's interest vector into redis storage
        """

        key = self._key_format.format(id=user_id, name=vector_name)
        self._redis.hmset(key, vector)

    def _load_interest_vector(self, user_id: int,
                              vector_name: str) -> Dict[int, int]:
        """
            Load user's interest vector from redis storage
        """

        key = self._key_format.format(id=user_id, name=vector_name)
        raw_data = self._redis.hmget(key)

        return {
            int(key): int(value) for key, value in raw_data.items()
        }

    @event_handler('api', 'user_registered')
    def handle_user_registration(self, user):
        """
            Called within a user registration to init their interest vectors
        """

        award_vector = dict.fromkeys(user['stack'],
                                     self._award_for_registration)
        event_category_vector = dict.fromkeys(self._event_category_range, 1)
        event_category_vector.update(award_vector)
        event_type_vector = dict.fromkeys(self._event_type_range, 1)

        self._dump_interest_vector(user['id'], 'event_categories',
                                   event_category_vector)
        self._dump_interest_vector(user['id'], 'event_types',
                                   event_type_vector)

    @event_handler('api', 'event_visited')
    def handle_users_visit(self, payload):
        """
            Called within a user event visit to update their interest vectors
        """

        award = self._award_for_visit.get(payload['visit_type'], 0)
        event_category_key = self._key_format.format(id=payload['user_id'],
                                                     name='event_categories')
        event_type_key = self._key_format.format(id=payload['user_id'],
                                                 name='event_types')

        for category in payload['categories']:
            self._redis.hincrby(event_category_key, category, award)

        self._redis.hincrby(event_type_key, payload['event_type'], award)

    @event_handler('api', 'user_stack_changed')
    def handle_user_stack_change(self, payload):
        """
            Called within a user stack change to update their interest vectors
        """

        key = self._key_format.format(id=payload['user_id'],
                                      name='event_categories')

        for category in payload['old_stack']:
            self._redis.hincrby(key, category, -self._award_for_registration)

        for category in payload['new_stack']:
            self._redis.hincrby(key, category, self._award_for_registration)

    @rpc
    def get_recommendations(self, payload):
        """
            Make events recommendations for a user based
            on info collected by recommendation service
        """

        session = Session()

        event_category_vector = self._load_interest_vector(payload['user_id'],
                                                           'event_categories')
        event_types_vector = self._load_interest_vector(payload['user_id'],
                                                        'event_types')

        categories_sum = sum(event_category_vector.values())
        types_sum = sum(event_types_vector.values())

        all_events_query = session.query(Event).filter(
            Event.event_time >= datetime.utcnow()
        )
        total_events_num = all_events_query.count()

        result_query = session.query.filter(False)

        for category, category_score in event_category_vector.items():
            category_percent = category_score / categories_sum

            category_events_query = all_events_query.filter(
                Event.categories.any(EventCategory.id == category)
            )

            for event_type, event_type_score in event_types_vector.items():
                type_percent = event_type_score / types_sum
                limit = total_events_num * category_percent * type_percent

                filtered_query = category_events_query.filter(
                    Event.event_type_id == event_type
                ).limit(limit)

                result_query = result_query.union(filtered_query)

        result_query = result_query.order_by(Event.event_time)

        Session.remove()

        # TODO: check if it will be sent over RabbitMQ
        return result_query
