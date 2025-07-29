import grpc
from concurrent import futures
import meteoServer_pb2
import meteoServer_pb2_grpc

from load_balancer_service import load_balancer_service


#clase del servicio LB que delega a la clase LB serice
class LoadBalancerServiceServicer(meteoServer_pb2_grpc.LoadBalancerServiceServicer):
    
    def SendMeteoData(self,RawMeteoData, context):
        load_balancer_service.send_meteo_data(RawMeteoData)
        response = meteoServer_pb2.google_dot_protobuf_dot_empty__pb2.Empty()        
        return response

    def SendPollutionData(self,RawPollutionData, context):
        load_balancer_service.send_pollution_data(RawPollutionData)
        response = meteoServer_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response
        
        
def main():

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    meteoServer_pb2_grpc.add_LoadBalancerServiceServicer_to_server(LoadBalancerServiceServicer(), server)   
    print('Starting server. Listening on port 50051.')
    server.add_insecure_port('[::]:50051')
    server.start()

    try:
        while True:
            server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)
        
        
if __name__ == "__main__":
    main()