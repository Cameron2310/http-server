import http_message
import datetime


def handle_path(request: http_message.Request):
    match request.path:
        case "/echo":
            base_str = f"{request.http_version} 200 OK\r\n"
            base_str += f"Server: Test\r\nDate:{datetime.datetime.now()}\r\n\n"
            base_str += f"{request.body}\n"

            return base_str.encode()

        case _:
            return f"{request.http_version} 400 Path not found\r\n".encode()
