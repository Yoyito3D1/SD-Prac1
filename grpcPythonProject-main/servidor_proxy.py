import datetime
import grpc
import redis
import time
from statistics import mean, stdev

from numpy import double

import meteoServer_pb2
import meteoServer_pb2_grpc

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
        self.terminal_list = ['localhost:50057', 'localhost:50058']


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
                    
                    pollution_results = meteoServer_pb2.PollutionResults(time=min_time, avg=p_avg, desv=p_std)
                    wellness_results = meteoServer_pb2.WellnessResults(time=min_time, avg=m_avg, desv=m_std)

                    for terminal_address in self.terminal_list:
                        channel_stub = grpc.insecure_channel(terminal_address)
                        server_terminal = meteoServer_pb2_grpc.TerminalServiceStub(channel_stub)
                        print(f'Sent from proxy to terminal, time: {min_time}, pollution_avg: {p_avg}, pollution_std: {p_std}, wellness_avg: {m_avg}, wellness_std: {m_std}.')
                        server_terminal.SendResults(meteoServer_pb2.Results(wellness_results=wellness_results, pollution_results=pollution_results))

                    self.redis_con.flushdb()
                self.last_timestamp = current_time
            time.sleep(self.window_time)



if __name__ == "__main__":
    
    print('STARTING PROXY')
    proxy = ProxyService()
    proxy.run()
