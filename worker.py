import pika
import time

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Guarantees that the queue will survive a RabbitMQ node restart with durable=True:
# needs to be applied to both the producer and consumer code
channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    # Guarantees that if a worker dies all unacknowledged messages will be redelivered:
    ch.basic_ack(delivery_tag=method.delivery_tag)


# don't dispatch a new message to a worker until it has processed and acknowledged the previous one.
# Instead, it will dispatch it to the next worker that is not still busy.
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)

channel.start_consuming()