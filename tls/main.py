import socket
from . import client, server


def handle_https_request(request: bytes, client_sock: socket.socket):
    client_hello = client.parse_client_message(request)
    server_hello = server.create_server_hello(client_hello.session_id)

    client_sock.send(bytes(server_hello))
