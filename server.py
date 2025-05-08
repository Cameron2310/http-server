import socket
import threading
from routing import handle_path
from http_message import Request


def handle_request(client_sock: socket.socket, request_id: int):
    try:
        data = client_sock.recv(1024)
        print("\n\ndata ------> ", data)
        request = Request(data)

        response = handle_path(request)
        print(f"\n\nresponse to request {request_id}\n", response)
        client_sock.sendall(response)

    finally:
        client_sock.close()


def start_server(port: int, max_connections: int):
    request_count = -1

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.bind(("localhost", port))
        server_sock.listen(max_connections)

        while True:
            client_sock, _ = server_sock.accept()
            request_count += 1

            try:
                t = threading.Thread(target=handle_request, args=((client_sock, request_count)))
                t.daemon = True
                t.start()
                
            except Exception as e:
                print(f"Exception received\n{e}")
                print("Shutting down...")
                break


if __name__ == "__main__":
    start_server(8000, 5)
