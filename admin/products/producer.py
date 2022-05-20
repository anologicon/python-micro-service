import pika, os, json
from dotenv import load_dotenv
from pika.exceptions import ChannelWrongStateError, StreamLostError

load_dotenv()

AMQP_URI = os.environ.get('AMQP_URI')

params = pika.URLParameters(AMQP_URI)

def pub(method, body):
    properties = pika.BasicProperties(method)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties)
    connection.close()
   
