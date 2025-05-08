import argparse
import socket
import threading
from routing import handle_path
from http_message import Request


def handle_request(client_sock, request_id: int, is_parallel):
    try:
        data = client_sock.recv(1024)
        print("\n\ndata ------> ", data)
        request = Request(data)

        response = handle_path(request)
        print(f"\n\nresponse to request {request_id}\n", response)
        client_sock.sendall(response)

    finally:
        if is_parallel:
            client_sock.close()


def start_server(port: int, max_connections: int, is_parallel: bool):
    request_count = -1

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.bind(("localhost", port))
        server_sock.listen(max_connections)

        while True:
            client_sock, addr = server_sock.accept()
            request_count += 1

            try:
                if is_parallel:
                    t = threading.Thread(target=handle_request, args=((client_sock, request_count, is_parallel)))
                    t.daemon = True
                    t.start()
                
                else:
                    print("serial implementation running...")
                    handle_request(client_sock, request_count, is_parallel)

            finally:
                if not is_parallel:
                    print("shutting down connection...")
                    client_sock.shutdown(socket.SHUT_WR)
                    client_sock.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", help="run each request on it's own thread", action="store_true")
    args = parser.parse_args()
    
    is_parallel = True if args.c else False
    start_server(8000, 5, is_parallel)
