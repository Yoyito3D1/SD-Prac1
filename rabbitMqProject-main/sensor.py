import pika
import json
import time
from meteo_utils import MeteoDataDetector


def send_data(sensor, channel):
    detector = MeteoDataDetector()
    while True:
        timestamp = int(time.time())        
        meteo_data = detector.analyze_air()
        temperature = meteo_data.get('temperature')
        humidity = meteo_data.get('humidity')
        data = {
            'id': sensor,
            'data_type': 'meteo',
            'temperature': temperature,
            'humidity': humidity,
            'timestamp': timestamp
        }
        message = json.dumps(data)
        channel.basic_publish(exchange='', routing_key='data_queue', body=message)

        timestamp = int(time.time())
        pollution_data = detector.analyze_pollution()
        co2 = pollution_data.get('co2')
        data = {
            'id': sensor,
            'data_type': 'pollution',
            'co2': co2,
            'timestamp': timestamp
        }  
        message = json.dumps(data)
        channel.basic_publish(exchange='', routing_key='data_queue', body=message)

        time.sleep(2)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='data_queue')
    send_data(1,channel=channel)    
    connection.close()
    
    
if __name__ == "__main__":
    main()
