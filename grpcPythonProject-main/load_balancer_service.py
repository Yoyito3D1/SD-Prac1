import random
from queue import Queue
import multiprocessing
import grpc
import meteoServer_pb2
import meteoServer_pb2_grpc


class loadBalancerService:

    def __init__(self):
       self.port_list = ['localhost:50052', 'localhost:50053', 'localhost:50054']
       self.index = 0
       self.quantum = 5
       self.lock = multiprocessing.Lock()
       
    def send_meteo_data(self, RawMeteoData):
        port = self.select_next_server()

        print(port)
        
        channel = grpc.insecure_channel(port)
        stub = meteoServer_pb2_grpc.ProcessServiceStub(channel)
        stub.ProcessMeteoData(RawMeteoData)
        channel.close()
        
        return 'Done'

    def send_pollution_data(self, RawPollutionData):
        port = self.select_next_server()

        print(port)

        channel = grpc.insecure_channel(port)
        stub = meteoServer_pb2_grpc.ProcessServiceStub(channel)
        stub.ProcessPollutionData(RawPollutionData)
        channel.close()

        return 'Done'
    
    
    
    def select_next_server(self):
        #sincronizamos quantum y indice
        with self.lock:
            self.quantum-= 1
            
            if self.quantum == 0:
                self.index = (self.index + 1) % len(self.port_list)
                self.quantum = 5
                
            port = self.port_list[self.index]
    
        return port
        

load_balancer_service = loadBalancerService()