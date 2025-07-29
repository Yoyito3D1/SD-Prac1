import grpc
import meteoServer_pb2
import meteoServer_pb2_grpc
from meteo_utils import MeteoDataDetector
import time
import multiprocessing
from google.protobuf.timestamp_pb2 import Timestamp

N_SENS = 2

def send_meteo_data(sensor):
    detector = MeteoDataDetector()
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = meteoServer_pb2_grpc.LoadBalancerServiceStub(channel)
        while True:
            timestamp = time.time()
            timestamp = int(timestamp)
            meteo_data = detector.analyze_air()
            temperature = meteo_data.get('temperature')
            humidity = meteo_data.get('humidity')
            RawMeteoData = meteoServer_pb2.RawMeteoData(id=sensor,temperature=temperature,humidity=humidity, timestamp= timestamp)
            stub.SendMeteoData(RawMeteoData)
            time.sleep(2)

def send_pollution_data(sensor):
    detector = MeteoDataDetector()
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = meteoServer_pb2_grpc.LoadBalancerServiceStub(channel)
        while True:
            timestamp = time.time()
            timestamp = int(timestamp)
            pollution_data = detector.analyze_pollution()
            co2 = pollution_data.get('co2')
            RawPollutionData = meteoServer_pb2.RawPollutionData(id=sensor, co2=co2, timestamp= timestamp)
            stub.SendPollutionData(RawPollutionData)
            time.sleep(2)
    
def main():

    for i in range(N_SENS):
        process_name_air = f"SensorAir{i}"
        process_air = multiprocessing.Process(target=send_meteo_data, args=(process_name_air,))
        process_air.start()

        process_name_pol = f"SensorPol{i}"
        process_pol = multiprocessing.Process(target=send_pollution_data, args=(process_name_pol,))
        process_pol.start()


if __name__ == "__main__":
    main()
