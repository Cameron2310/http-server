import logging

logger = logging.getLogger("tls_server")


def determine_file_type(first_four_bytes: bytes):
    file_types = {
        "ffd8ffe0": "jpg" 
    }

    hex_str = first_four_bytes.hex()
    try:
        return file_types[hex_str]

    except Exception as e:
        logger.exception(f"Exception {e}")
