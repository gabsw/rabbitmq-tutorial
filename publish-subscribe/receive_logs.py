import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

#  let the server choose a random queue name: queue=''
# once the consumer connection is closed, the queue should be deleted: exclusive=True
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# A binding is a relationship between an exchange and a queue
# tells the exchange to send messages to our queue
channel.queue_bind(exchange='logs', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r" % body)


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
