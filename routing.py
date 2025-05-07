import datetime
import http_message


def handle_path(request: http_message.Request):
    match request.path:
        case "/echo":
            base_str = [f"{request.http_version} 200 OK"]
            base_str.append(f"Date: {datetime.datetime.now()}\r\nServer: Test\r\nContent-Length: {len(request.body)}\r\nContent-Type: text/plain")
            base_str.append("")  # Empty line to separate headers and body
            base_str.append(f"{request.body}")

            new_str = "\r\n".join(base_str)
            return new_str.encode()

        case _:
            return f"{request.http_version} 400 Path not found\r\n".encode()
