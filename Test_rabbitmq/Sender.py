import pika
import json

with open('events.json',) as f:
    data = [json.loads(line) for line in f]
data = json.dumps(data)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='my_queue')

channel.basic_publish(exchange='',
                      routing_key='my_queue',
                      body=data)
print(" [x] Sent data")
connection.close()
