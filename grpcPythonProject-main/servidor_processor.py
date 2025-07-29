import grpc
from concurrent import futures
import meteoServer_pb2
import meteoServer_pb2_grpc
import multiprocessing
from processor_service import processor_service

class ProcessorServiceServicer(meteoServer_pb2_grpc.ProcessServiceServicer):
    
    def ProcessMeteoData(self,RawMeteoData, context):
        processor_service.process_meteo_data(RawMeteoData)
        response = meteoServer_pb2.google_dot_protobuf_dot_empty__pb2.Empty()        
        return response

    def ProcessPollutionData(self,RawPollutionData, context):
        processor_service.process_pollution_data(RawPollutionData)
        response = meteoServer_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response  
    
def iniciar_servidor(port):
    try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        meteoServer_pb2_grpc.add_ProcessServiceServicer_to_server(ProcessorServiceServicer(), server)
        print(f'Starting server. Listening on port {port}.')
        server.add_insecure_port(f'[::]:{port}')
        server.start()
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)
   
def main():
    
    portlist = [50052, 50053, 50054]
    for port in portlist:
        p = multiprocessing.Process(target=iniciar_servidor, args=(port,))
        p.start()
   
        
if __name__ == "__main__":
    main()