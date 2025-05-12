from os import urandom
import utils


def create_client_hello_extensions():
    name = "localhost"
    server_name_bytes = b'0x00' 
    server_name = (len(name) + 3).to_bytes(2, "big") + b'0x00' + (len(name)).to_bytes(2, "big") + bytes(name, "utf-8")
    
    server_name_bytes += (len(server_name)).to_bytes(2, "big") + server_name
    group_bytes = b'0x0a\\0x00\\0x02\\0x00\\0x1d'
    supported_algorithms = b'0x0d\\0x00\\0x12\\0x04\\0x03\\0x08\\0x04\\0x04\\0x01\\0x05\\0x03\\0x08\\0x05\\0x01\\0x08\\0x06\\0x01\\0x02\\0x01'
    
    keys = utils.generate_key_pair()
    key_bytes = b'0x33' + (len(keys.public_key) + 4).to_bytes(2, "big") + b"0x1d" + (len(keys.public_key)).to_bytes(2, "big") + keys.public_key
    psk_bytes = b'0x2d\\0x01\\0x01'
    tls_version_bytes = b'0x2b\\0x02\\0x03\\0x04'

    return server_name_bytes + group_bytes + supported_algorithms + key_bytes + psk_bytes + tls_version_bytes 


def create_client_hello():
    # handshake record (0x16)
    handshake_record = b'0x16'

    # tls version (0x03, 0x01) (TLS 1.0)
    tls_version = b'0x03\\0x01'
    client_version = b'0x03\\0x03'
    
    client_random = urandom(32)
    session_id = b'0x00'
    cipher_suites = b'0x00\\0x02\\0x13\\0x01'

    # TLS 1.3 does not allow compression, so this is a null value
    compression_methods = b'0x01\\0x00'
    extensions = create_client_hello_extensions()
    handshake = client_version + client_random + session_id + cipher_suites + compression_methods + (len(extensions)).to_bytes(2, "big") + extensions

    return handshake_record + tls_version + (len(handshake) + 4).to_bytes(2, "big") + b"0x01\\0x00" + (len(handshake)).to_bytes(2, "big") + handshake
