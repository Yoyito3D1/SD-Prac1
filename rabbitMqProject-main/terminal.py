import sys
import pika

def callback(ch, method, properties, body):
    print(f'Received message: {body.decode()}')

def consume_results(queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    print(f'Waiting for messages from queue: {queue_name}')
    channel.start_consuming()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError('Queue name not provided')

    queue_name = sys.argv[1]
    print('STARTING TERMINAL')
    consume_results(queue_name)
