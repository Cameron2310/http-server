from os import urandom
import utils


def create_client_hello_extensions():
    name = "localhost"
    server_name = (len(name) + 3).to_bytes(2, "big") + b'\x00' + (len(name)).to_bytes(2, "big") + name.encode()
    
    server_name_bytes = utils.create_extension(0x0, server_name)
    group_bytes = utils.create_extension(0x0a, [0x00, 0x02, 0x00, 0x1d])
    supported_algorithms = utils.create_extension(0x0d, [0x00, 0x12, 0x04, 0x03, 0x08, 0x04, 0x04, 0x01, 0x05, 0x03, 0x08, 0x05, 0x05, 0x01, 0x08, 0x06, 0x06, 0x01, 0x02, 0x01])
    
    keys = utils.generate_key_pair()
    print("length of key ", len(keys.public_key.public_bytes_raw()))
    key_bytes = utils.create_extension(0x33, (len(keys.public_key.public_bytes_raw()) + 4).to_bytes(2, "big") + 0x1d.to_bytes(2, "big") + (len(keys.public_key.public_bytes_raw())).to_bytes(2, "big") + keys.public_key.public_bytes_raw())
    psk_bytes = utils.create_extension(0x2d, [0x01, 0x01])
    tls_version_bytes = utils.create_extension(0x2b, [0x02, 0x03, 0x04])

    return server_name_bytes + group_bytes + supported_algorithms + key_bytes + psk_bytes + tls_version_bytes 


def create_client_hello():
    handshake_record = [0x16]

    # tls version (0x03, 0x01) (TLS 1.0)
    tls_version = [0x03, 0x01]
    client_version = [0x03, 0x03]
    
    client_random = urandom(32)
    client_random_bytes = [int(i) for i in client_random]

    session_id = [0x00]
    cipher_suites = [0x00, 0x02, 0x13, 0x01]

    # TLS 1.3 does not allow compression, so this is a null value
    compression_methods = [0x01, 0x00]
    extensions = create_client_hello_extensions()
    handshake = client_version + client_random_bytes + session_id + cipher_suites + compression_methods + [int(i) for i in (len(extensions)).to_bytes(2, "big")] + extensions

    return handshake_record + tls_version + [int(i) for i in (len(handshake) + 4).to_bytes(2, "big")] + [0x01, 0x00] + [int(i) for i in (len(handshake)).to_bytes(2, "big")] + handshake

print(create_client_hello())
