import socket
from http_message import create_http_response


def start_server(port: int, max_connections: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("localhost", port))
        s.listen(max_connections)

        while True:
            conn, addr = s.accept()

            try:
                print('Connected by', addr)
                data = conn.recv(1024)
                conn.sendall(create_http_response(200, "Welcome to the Jungle!"))
            finally:
                conn.close()


start_server(8000, 10)
