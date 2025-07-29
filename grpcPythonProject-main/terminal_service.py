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

class TerminalService:
    def send_results(self, results):
        print("Received results:")
        print("Wellness Results:")
        print("Time:", results.wellness_results.time)
        print("Average:", results.wellness_results.avg)
        print("Standard Deviation:", results.wellness_results.desv)
        print("Pollution Results:")
        print("Time:", results.pollution_results.time)
        print("Average:", results.pollution_results.avg)
        print("Standard Deviation:", results.pollution_results.desv)
        return 'Done'


terminal_service = TerminalService()