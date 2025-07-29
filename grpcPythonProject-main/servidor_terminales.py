import grpc
from concurrent import futures
import meteoServer_pb2
import meteoServer_pb2_grpc
import multiprocessing
from terminal_service import terminal_service

class TerminalServiceServicer(meteoServer_pb2_grpc.TerminalServiceServicer):
    
    def SendResults(self,Results, context):
        terminal_service.send_results(Results)
        response = meteoServer_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response  
    
def iniciar_servidor(port):
    try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        meteoServer_pb2_grpc.add_TerminalServiceServicer_to_server(TerminalServiceServicer(), server)
        print(f'Starting TERMINAL server. Listening on port {port}.')
        server.add_insecure_port(f'[::]:{port}')
        server.start()
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)
   
def main():
    
    portlist = [50057, 50058]
    for port in portlist:
        p = multiprocessing.Process(target=iniciar_servidor, args=(port,))
        p.start()
   
        
if __name__ == "__main__":
    main()