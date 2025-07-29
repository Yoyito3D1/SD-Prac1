import datetime
import redis
import time
from statistics import mean, stdev
import pika

from numpy import double

def strip(string):
    ls = []
    for item in string:
        ls.append(double(item.decode()[1:]))
    return ls

class ProxyService:
    def __init__(self):
        self.redis_con = redis.Redis('localhost', port=6379, db=0)
        self.window_time = 10
        self.window_length = 10
        self.last_timestamp = datetime.datetime.now()
        self.queue_list = ['terminal1_queue', 'terminal2_queue']
        self.rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.rabbitmq_channel = self.rabbitmq_connection.channel()

    def get_values(self, keys):
        p_values = []
        m_values = []
        for key in keys:
            value = float(self.redis_con.get(key))
            if key.startswith(b'p'):
                p_values.append(value)
            elif key.startswith(b'm'):
                m_values.append(value)
        
        p_avg = mean(p_values) if p_values else 0
        m_avg = mean(m_values) if m_values else 0
        p_std = stdev(p_values) if len(p_values) >= 2 else 0 #varianza necesita 2 valores por defecto sino da error
        m_std = stdev(m_values) if len(m_values) >= 2 else 0
        
        return p_avg, m_avg, p_std, m_std

    def publish_results(self, queue_name, results):
        self.rabbitmq_channel.basic_publish(exchange='', routing_key=queue_name, body=results)

    def run(self):
        while True:
            current_time = datetime.datetime.now()
            time_diff = (current_time - self.last_timestamp).total_seconds()
            if time_diff >= self.window_time:
                keys = self.redis_con.keys()
                if keys:
                    p_avg, m_avg, p_std, m_std = self.get_values(keys)

                    min_time = min(strip(keys)) + self.window_time
                    print('MIN_TIME:', min_time)

                    pollution_results = f"Pollution Results: time={min_time}, avg={p_avg}, desv={p_std}"
                    wellness_results = f"Wellness Results: time={min_time}, avg={m_avg}, desv={m_std}"

                    for queue_name in self.queue_list:
                        if wellness_results:
                            self.publish_results(queue_name, wellness_results)
                            print(f'Sent from proxy to queue {queue_name}: {wellness_results}')
                        if pollution_results:
                            self.publish_results(queue_name, pollution_results)
                            print(f'Sent from proxy to queue {queue_name}: {pollution_results}')

                    self.redis_con.flushdb()
                self.last_timestamp = current_time
            time.sleep(self.window_time)

if __name__ == "__main__":
    print('STARTING PROXY')
    proxy = ProxyService()
    proxy.run()
