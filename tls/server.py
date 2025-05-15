from collections import namedtuple
from os import urandom
from . import utils

ServerHello = namedtuple("ServerHello", ["message", "private_key"])


def create_server_hello_extensions(keys: utils.KeyPair):
    supported_versions = utils.create_extension(0x2b, [0x03, 0x04])

    len_key = (len(keys.public_key.public_bytes_raw())).to_bytes(2, "big")
    key_bytes = utils.create_extension(0x33, 0x1d.to_bytes(2, "big") + len_key + keys.public_key.public_bytes_raw())
    
    return supported_versions + key_bytes 


def create_server_hello(session_id) -> ServerHello:
    handshake_record = [0x16]
    protocol_version = [0x03, 0x03]
    keys = utils.generate_key_pair()

    server_tls_version = [0x03, 0x03]  # tls version 1.2
    server_random = [int(i) for i in urandom(32)]

    cipher_suite = [0x13, 0x02]
    compression_method = [0x00]

    extensions = create_server_hello_extensions(keys)
    handshake = server_tls_version + server_random + [0x20] + [int(i) for i in session_id] + cipher_suite + compression_method + [int(i) for i in (len(extensions)).to_bytes(2, "big")] + extensions 

    handshake_data = [int(i) for i in (len(handshake) + 4).to_bytes(2, "big")]
    len_handshake = [int(i) for i in (len(handshake)).to_bytes(2, "big")]

    return ServerHello(handshake_record + protocol_version + handshake_data + [0x02, 0x00] + len_handshake + handshake, keys.private_key)


def create_wrapped_record(shs_key: bytes, shs_iv: bytes, data: bytes, additional: bytes = None):
    handshake_record = bytes(0x17)
    protocol_version = bytes([0x03, 0x03])
    encrypted_data = utils.encrypt(shs_key, shs_iv, data, additional)

    record = handshake_record + protocol_version + (len(encrypted_data).to_bytes(2, "big")) + encrypted_data
    print("length of encrypted_data -----> ", len(encrypted_data))
    return record
    
