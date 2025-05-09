from datetime import datetime


class Request:
    def __init__(self, request: bytes):
        str_request = request.decode()
        parsed_request = str_request.split("\r\n")
        start_line = parsed_request[0].split()
        
        self.method = start_line[0]
        self.path = start_line[1]
        self.http_version = start_line[2]

        self.headers = parsed_request[1: parsed_request.index("")]
        self.body = parsed_request[parsed_request.index("") + 1].encode()


    def find_header(self, header: str):
        for h in self.headers:
            if header in h:
                spl_header = h.split()
                return spl_header[1]

        return ""


def create_response(response_code: int, response_message: str, content_type="text/plain", body=""):
    http_version = "HTTP/1.1"
    content_len = len(body)

    headers = [f"Data: {datetime.now()}", "Server: Test", f"Content-Length: {content_len}", f"Content-Type: {content_type}"]
    
    response = f"{http_version} {response_code} {response_message}\r\n"
    for h in headers:
        response += f"{h}\r\n"
    
    response += "\r\n"
    
    if not isinstance(body, str):
        return response.encode() + body

    return (response + body).encode()
