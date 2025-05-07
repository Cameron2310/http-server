import socket
from routing import handle_path
from http_message import Request


def handle_request(client_sock, request_id: int):
    data = client_sock.recv(1024)
    print("\n\ndata ------> ", data)
    request = Request(data)
    response = handle_path(request)
    print(f"\n\nresponse to request {request_id}\n", response)
    client_sock.sendall(response)
    

def start_server(port: int, max_connections: int):
    request_count = -1

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.bind(("localhost", port))
        server_sock.listen(max_connections)

        while True:
            client_sock, addr = server_sock.accept()
            request_count += 1

            try:
                handle_request(client_sock, request_count)

            finally:
                print("closing connection...")
                client_sock.shutdown(socket.SHUT_WR)
                client_sock.close()

                
start_server(8000, 5)
