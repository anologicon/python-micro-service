import pika
import os

AMQP_URI = os.environ.get('AMQP_URI')

params = pika.URLParameters(AMQP_URI)

connection = pika.BlockingConnection(params)

channel = connection.channel()

def pub():
    channel.basic_publish(exchange='', routing_key='main', body='Hello World Main!')