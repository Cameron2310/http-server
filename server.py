import socket
from routing import handle_path
from http_message import Request


def handle_request(client_sock):
    data = client_sock.recv(1024, socket.MSG_DONTWAIT)

    while data:
        try:
            request = Request(data)
            response = handle_path(request)
            client_sock.send(response, socket.MSG_DONTWAIT)
            
            data = client_sock.recv(1024, socket.MSG_DONTWAIT)
            print(data)
        except BlockingIOError:
            pass
        except Exception:
            break

    print("ending loop")


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
                client_sock.close()
                
start_server(8000, 20)
