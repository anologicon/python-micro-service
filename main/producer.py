import pika, os, json

AMQP_URI = os.environ.get('AMQP_URI')

params = pika.URLParameters(AMQP_URI)

connection = pika.BlockingConnection(params)

channel = connection.channel()

def pub(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body), properties=properties)