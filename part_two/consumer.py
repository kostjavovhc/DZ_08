import pika
from models import Contact, connect
from bson import ObjectId


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='email_sender')

    def callback(ch, method, properties, body):
        model_id = ObjectId(body)
        model = Contact.objects.get(id=model_id)
        print(f"№{method.delivery_tag} email send to {model.email}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        model.update(email_send=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='email_sender', on_message_callback=callback)

    print('Start consuming')
    channel.start_consuming()


if __name__ == '__main__':
    main()