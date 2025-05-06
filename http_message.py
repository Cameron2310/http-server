class Request:
    def __init__(self, request: bytes):
        str_request = request.decode()
        parsed_request = str_request.split("\r\n")
        start_line = parsed_request[0].split()
        
        self.method = start_line[0]
        self.path = start_line[1]
        self.http_version = start_line[2]

        self.headers = parsed_request[1: parsed_request.index("")]
        self.body = parsed_request[parsed_request.index("") + 1]
