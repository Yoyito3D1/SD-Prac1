import pika

def view_queue(queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declara la cola si no existe
    channel.queue_declare(queue=queue_name)

    # Obtiene el número de mensajes en la cola
    method_frame = channel.queue_declare(queue=queue_name, passive=True)
    message_count = method_frame.method.message_count

    print(f"Número de mensajes en la cola '{queue_name}': {message_count}")

    # Itera sobre los mensajes en la cola y muestra su contenido
    for _ in range(message_count):
        method_frame, _, body = channel.basic_get(queue=queue_name, auto_ack=False)
        if method_frame is not None:
            print(f"Mensaje: {body.decode()}")

    connection.close()

# Llamada a la función para ver el contenido de la cola 'data_queue'
view_queue('data_queue')

