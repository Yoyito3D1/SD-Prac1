import random
import grpc
import meteoServer_pb2
import meteoServer_pb2_grpc
import concurrent.futures
import time
from concurrent import futures
from meteo_utils import MeteoDataProcessor
import redis
import multiprocessing


class ProcessorService:
    def __init__(self):
        self.processor = MeteoDataProcessor()
        self.r = redis.Redis(host='localhost', port=6379, db=0)
        self.lock = multiprocessing.Lock()  

    def process_meteo_data(self, RawMeteoData):
        wellness_data = self.processor.process_meteo_data(RawMeteoData)
        with self.lock:  
            self.r.set(f'm{str(RawMeteoData.timestamp)}', wellness_data)
        return 'Done'

    def process_pollution_data(self, RawPollutionData):
        pollution_data = self.processor.process_pollution_data(RawPollutionData)
        
        with self.lock: 
            self.r.set(f'p{str(RawPollutionData.timestamp)}', pollution_data)
        return 'Done'

processor_service = ProcessorService()