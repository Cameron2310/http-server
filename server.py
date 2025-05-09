import socket
import threading
from routing import handle_path
from http_message import Request


def handle_request(client_sock: socket.socket, request_id: int):
    try:
        batch_size = 2048
        data = client_sock.recv(batch_size)
        
        request = Request(data)
        content_length = int(request.find_header("Content-Length")) - batch_size
       
        if content_length > batch_size:
            byte_list = [request.body]

            while content_length > 0:
                content_length -= batch_size
                byte_list.append(client_sock.recv(batch_size))
            
            request.body = b"".join(byte_list)

        response = handle_path(request)
        print(f"\nresponding to request {request_id}")
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
