from os import getenv

from nameko.standalone.events import event_dispatcher

_dispatch = event_dispatcher({
    'AMQP_URI': 'pyamqp://{user}:{password}@{host}'.format(
        user=getenv('RABBITMQ_DEFAULT_USER'),
        password=getenv('RABBITMQ_DEFAULT_PASS'),
        host=getenv('RABBITMQ_HOST')
    )
})

dispatch = lambda event: _dispatch('crawlers', 'new_event', event)
