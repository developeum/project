import pika
import json
import pandas as pd
from normalize import Normalize
from detect_types import Detect_type

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='my_queue')

def callback(ch, method, properties, body):
    print(" [x] Received data")
    data = body.decode('utf8')
    new_data = json.loads(data)
    events_df = pd.DataFrame(new_data)
    events_df = Normalize(events_df)
    events_df = Detect_type(events_df)


channel.basic_consume(queue='my_queue',
                      auto_ack=True,
                      on_message_callback=callback)

print(' [*] Waiting for messages. To exit interrupt the kernel')
channel.start_consuming()
