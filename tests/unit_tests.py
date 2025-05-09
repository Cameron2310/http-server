import requests
import threading
import time
import pytest
import sys
from utils import generate_basic_http_request, generate_body

sys.path.append("../")
import file_type
import http_message
import server

@pytest.mark.parametrize("file_bytes, answer", [(b'\xff\xd8\xff\xe0', "jpg")])
def test_determine_file_type(file_bytes: bytes, answer: str):
    # Arrange
    # Act
    # Assert
    assert file_type.determine_file_type(file_bytes) == answer


@pytest.mark.parametrize("header, is_found", [("User-Agent", True), ("Test", False)])
def test_find_header(header: str, is_found: bool):
    # Arrange
    request = http_message.Request(generate_basic_http_request())

    # Act
    response = request.find_header(header)
    result = True if response else False

    # Assert
    assert result == is_found


class TestServerClientIntegration:
    @classmethod
    def setup_class(cls):
        server_thread = threading.Thread(target=server.start_server, args=(8000, 5))
        server_thread.daemon = True
        server_thread.start()
        time.sleep(1)


    @pytest.mark.parametrize("relative_path, expected_status_code", [("echo", 200), ("/", 400)])
    def test_basic_request(self, relative_path: str, expected_status_code: int):
        # Arrange
        # Act
        # Assert
        assert requests.get(f"http://localhost:8000/{relative_path}").status_code == expected_status_code


    @pytest.mark.parametrize("n_requests", [(10), (100), (1000)])
    def test_sending_multiple_requests(self, n_requests: int):
        # Arrange
        returned_codes = []
        
        # Act
        for _ in range(n_requests):
            returned_codes.append(requests.get("http://localhost:8000/echo").status_code)
       
        # Assert
        for r in returned_codes:
            assert r == 200

   
def make_get_request(body):
    while True:
        n_retries = 0
        
        try:
            response = requests.get("http://localhost:8000/echo", data=body)
            return response.text

        except Exception as e:
            print(f"Exception {e}\nRetrying connection...")
            n_retries += 1

            if n_retries > 5:
                break
            else:
                pass
