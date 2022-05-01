from dotenv import load_dotenv
import pika
import json
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin.settings')
django.setup()

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

from products.models import Product

AMQP_URI = str(os.environ.get('AMQP_URI'))
print(AMQP_URI)
params = pika.URLParameters(AMQP_URI)

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='admin')

def callback(ch, method, properties, body):
    print(" [x] Received")
    data = json.loads(body)
    print(data)

    if properties.content_type == 'product_liked':
        product = Product.objects.get(id=data)
        product.likes += 1
        product.save()
        print('Product likes increased!')

channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')

channel.start_consuming()
channel.close()