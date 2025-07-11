import http_message
import logging
from datetime import datetime
from file_type import determine_file_type

logger = logging.getLogger("tls_server")


def handle_path(request: http_message.Request) -> bytes:
    match request.path:
        case "/echo":
            return http_message.create_response(200, "OK", request.find_header("Content-Type"), request.body + b"\n")

        case "/upload_file":
            try:
                if not request.body:
                    return http_message.create_response(400, "No file in request")

                with open(f"./files/{datetime.now()}.{determine_file_type(request.body[0:4])}", "wb") as f:
                    f.write(request.body)

                return http_message.create_response(201, "Created", body="File successfully uploaded")

            except Exception as e:
                logger.exception(f"Exception {e}")
                return http_message.create_response(500, "Server Error")

        case "/file":
            with open("./imgs/cute-cat.jpg", "rb") as f:
                file = f.read()

            return http_message.create_response(200, "OK", "image/jpeg", file)

        case _:
            return http_message.create_response(400, "Path not found")
