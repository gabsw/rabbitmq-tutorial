import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Guarantees that the queue will survive a RabbitMQ node restart with durable=True:
# needs to be applied to both the producer and consumer code
channel.queue_declare(queue='task_queue', durable=True)

message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=2,  # make message persistent
    ))

#  If you need a stronger guarantee for persistence then you can use publisher confirms.
print(" [x] Sent %r" % message)
connection.close()
