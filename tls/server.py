from os import urandom
from typing import List
from . import utils


def create_server_hello_extensions():
    supported_versions = utils.create_extension(0x2b, [0x03, 0x04])

    keys = utils.generate_key_pair()
    len_key = (len(keys.public_key.public_bytes_raw())).to_bytes(2, "big")
    key_bytes = utils.create_extension(0x33, 0x1d.to_bytes(2, "big") + len_key + keys.public_key.public_bytes_raw())
    
    return supported_versions + key_bytes 


def create_server_hello(session_id) -> List[int]:
    handshake_record = [0x16]
    protocol_version = [0x03, 0x03]

    server_tls_version = [0x03, 0x03]  # tls version 1.2
    server_random = [int(i) for i in urandom(32)]
    # TODO: parse client hello for session id

    cipher_suite = [0x13, 0x02]
    compression_method = [0x00]

    extensions = create_server_hello_extensions()
    handshake = server_tls_version + server_random + [0x20] + [int(i) for i in session_id] + cipher_suite + compression_method + [int(i) for i in (len(extensions)).to_bytes(2, "big")] + extensions 

    print("session id ----> ", len([int(i) for i in session_id]))
    handshake_data = [int(i) for i in (len(handshake) + 4).to_bytes(2, "big")]
    len_handshake = [int(i) for i in (len(handshake)).to_bytes(2, "big")]

    return handshake_record + protocol_version + handshake_data + [0x02, 0x00] + len_handshake + handshake 
