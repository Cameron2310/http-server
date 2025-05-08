import http_message


def handle_path(request: http_message.Request):
    match request.path:
        case "/echo":
            return http_message.create_response(200, "OK", request.body)

        case "/file":
            with open("./cute-cat.jpg", "rb") as f:
                file = f.read()

            print("file -----> ", type(file))
            return http_message.create_response(200, "OK", "image/jpeg", file)

        case _:
            return http_message.create_response(400, "Path not found")
