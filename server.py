import socket
from routing import handle_path
from http_message import Request

def start_server(port: int, max_connections: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("localhost", port))
        s.listen(max_connections)

        while True:
            conn, addr = s.accept()

            try:
                print('Connected by', addr)
                data = conn.recv(1024)
               
                response = handle_path(Request(data))
                conn.sendall(response)

            finally:
                conn.close()


start_server(8000, 10)
