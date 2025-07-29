import pika
import json
import redis
from meteo_utils import MeteoDataProcessor
import time

class RawPollutionData:
    def __init__(self, co2, timestamp):
        self.co2 = co2
        self.timestamp = timestamp


class RawMeteoData:
    def __init__(self, temperature, humidity, timestamp):
        self.temperature = temperature
        self.humidity = humidity
        self.timestamp = timestamp


class ProcessorService:
    def __init__(self):
        self.processor = MeteoDataProcessor()
        self.r = redis.Redis(host='localhost', port=6379, db=0)

    def process_meteo_data(self, raw_meteo_data):
        wellness = self.processor.process_meteo_data(raw_meteo_data)
        timestamp = raw_meteo_data.timestamp
        self.r.set(f"m{timestamp}", wellness)  # Guardar en Redis con la key "m{timestamp}"
        print(f'{timestamp}')
        return 'Done'

    def process_pollution_data(self, raw_pollution_data):
        pollution = self.processor.process_pollution_data(raw_pollution_data)
        timestamp = raw_pollution_data.timestamp
        self.r.set(f"p{timestamp}", pollution)  # Guardar en Redis con la key "p{timestamp}"
        print(f'{timestamp}')

        return 'Done'


class RabbitMQConsumer:
    def __init__(self):
        self.processor_service = ProcessorService()
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='data_queue')

    def consume_data(self, ch, method, properties, body):
        data = json.loads(body.decode())
        data_type = data['data_type']
        timestamp = data['timestamp']

        if data_type == 'meteo':
            raw_meteo_data = RawMeteoData(
                temperature=data['temperature'],
                humidity=data['humidity'],
                timestamp=timestamp
            )
            self.processor_service.process_meteo_data(raw_meteo_data)
        elif data_type == 'pollution':
            raw_pollution_data = RawPollutionData(
                co2=data['co2'],
                timestamp=timestamp
            )
            self.processor_service.process_pollution_data(raw_pollution_data)

    def start_consuming(self):
        self.channel.basic_consume(queue='data_queue', on_message_callback=self.consume_data, auto_ack=True)
        print('Consuming data from the queue...')
        self.channel.start_consuming()


def main():
    RabbitMQConsumer().start_consuming()


if __name__ == "__main__":
    main()
