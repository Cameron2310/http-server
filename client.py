import socket

def connect_to_server(port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", port))
        s.sendall(b'Hello, world')
        data = s.recv(1024)

        print('Received', repr(data))


connect_to_server(8000)
