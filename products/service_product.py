import pika
import json
from .models import Product

def publish_products():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare the exchange for product data
    channel.exchange_declare(exchange='product_exchange', exchange_type='topic')

    # Fetch the products from the database
    products = Product.objects.all()
    product_list = [{
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': str(product.price),
        'stock': product.stock
    } for product in products]

    # Prepare the message
    message = {
        'products': product_list
    }

    # Publish the product list
    channel.basic_publish(
        exchange='product_exchange',
        routing_key='product.list',
        body=json.dumps(message)
    )

    print(f"Published product list: {product_list}")
    connection.close()

# Call the function to publish the products


# publish_products()


# import pika
# import json

# def callback(ch, method, properties, body):
#     print(method,ch,properties)
#     print(body,"body")

#     order_data = json.loads(body)
#     print(f"Received order for product reservation: {order_data}")
#     # Handle product reservation logic

# def consume_order_created():
#     connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
#     channel = connection.channel()

#     # Declare exchange and queue
#     channel.exchange_declare(exchange='service_exchange', exchange_type='topic')
#     channel.queue_declare(queue='product_service_queue')

#     # Bind queue to exchange with routing key
#     channel.queue_bind(exchange='service_exchange', queue='product_service_queue', routing_key='order.created')

#     # Subscribe to the queue
#     channel.basic_consume(queue='product_service_queue', on_message_callback=callback, auto_ack=True)
#     print("Waiting for messages in product service...")
#     channel.start_consuming()

# if __name__ == "__main__":
#     consume_order_created()
