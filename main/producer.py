import pika, os, json
from dotenv import load_dotenv
from pika.exceptions import ChannelWrongStateError

load_dotenv()

AMQP_URI = os.environ.get('AMQP_URI')

params = pika.URLParameters(AMQP_URI)

connection = pika.BlockingConnection(params)

channel = connection.channel()

def pub(method, body):
    properties = pika.BasicProperties(method)

    try:
        channel.basic_publish(exchange='', routing_key='admin',
                              body=json.dumps(body), properties=properties)
    except ChannelWrongStateError:
        connection.close()
        connection = pika.BlockingConnection(params)
        pub(method, body)
    
