import random
import string

def generate_basic_http_request():
    request = "GET / HTTP/1.1\r\n"
    headers = ["Host: localhost", "User-Agent: http-server.test", "Accept: */*"]
    
    for h in headers:
        request += h + "\r\n"

    return (request + "\r\n").encode()


def generate_body(length: int):
    return "".join([random.choice(string.ascii_letters + string.digits) for _ in range(length)])
