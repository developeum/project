import pika
import json
import pandas as pd
from classification.normalize import Normalize
from classification.detect_types import Detect_type

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='rpc_queue')

def on_request(ch, method, props, body):
    print(" [x] Received data")
    data = body.decode('utf8')
    new_data = json.loads(data)
    events_df = pd.DataFrame(new_data)
    events_df = Normalize(events_df)
    events_df = Detect_type(events_df)

    # classification

    response = events_df.to_dict(orient='records')
    response = json.dumps(response)
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                     props.correlation_id),
                     body=response)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume('rpc_queue', on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()
