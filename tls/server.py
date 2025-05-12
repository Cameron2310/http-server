from os import urandom


def create_server_hello_extensions():
    supported_versions = b'0x00\\0x02\\0x03\\0x04'



def create_server_hello():
    handshake_record = b'0x16'
    protocol_version = b'0x03\\0x03'

    handshake_header = b'0x02'
    server_tls_version = b'0x03\\0x03'  # tls version 1.2
    server_random = urandom(32)

    # TODO: parse client hello for session id

    cipher_suite = b'0x13\\0x02'
    compression_method = b'0x00'


