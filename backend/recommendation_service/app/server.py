from typing import Dict

from nameko.events import event_handler
# from nameko.rpc import rpc
from redis import Redis

from config import REDIS_HOST, REDIS_PORT


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
        event_category_vector = dict.fromkeys(self._event_category_range, 0)
        event_category_vector.update(award_vector)
        event_type_vector = dict.fromkeys(self._event_type_range, 0)

        self._dump_interest_vector(user['id'], 'event_categories',
                                   event_category_vector)
        self._dump_interest_vector(user['id'], 'event_types',
                                   event_type_vector)
