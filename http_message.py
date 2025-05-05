def create_http_response(resp_code: int, resp_mess: str) -> bytes:
    return f"HTTP/1.1 {resp_code} {resp_mess}\n".encode()
