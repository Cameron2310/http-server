import http_message
import datetime


def handle_path(request: http_message.Request):
    match request.path:
        case "/echo":
            base_str = [f"{request.http_version} 200 OK"]
            base_str.append(f"Server: Test\r\nDate:{datetime.datetime.now()}")
            base_str.append(f"{request.body}")

            new_str = "\r\n".join(base_str)
            return new_str.encode()

        case _:
            return f"{request.http_version} 400 Path not found\r\n".encode()
