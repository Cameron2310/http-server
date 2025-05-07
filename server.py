import socket
from routing import handle_path
from http_message import Request


def handle_request(client_sock):
    data = client_sock.recv(1024)
    print("retrieving data...", data)

    request = Request(data)
    response = handle_path(request)
    client_sock.send(response)
    

def start_server(port: int, max_connections: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.bind(("localhost", port))
        server_sock.listen(max_connections)

        while True:
            client_sock, addr = server_sock.accept()

            try:
                handle_request(client_sock)

            finally:
                print("closing connection...")
                client_sock.shutdown(socket.SHUT_WR)
                client_sock.close()

                
start_server(8000, 5)
