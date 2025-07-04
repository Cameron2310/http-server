from collections import namedtuple
from os import urandom
from . import utils

ServerHello = namedtuple("ServerHello", ["message", "private_key"])


def create_server_hello_extensions(keys: utils.KeyPair):
    supported_versions = utils.create_extension(0x2b, [0x03, 0x04])

    len_key = (len(keys.public_key.public_bytes_raw())).to_bytes(2, "big")
    public_key_raw = keys.public_key.public_bytes_raw()

    key_bytes = utils.create_extension(0x33, 0x1d.to_bytes(2, "big") + len_key + public_key_raw)
    
    return supported_versions + key_bytes 


def create_server_hello(session_id) -> ServerHello:
    handshake_record = [0x16]
    protocol_version = [0x03, 0x03]
    keys = utils.generate_key_pair()

    server_tls_version = [0x03, 0x03]  # tls version 1.2
    server_random = [int(i) for i in urandom(32)]

    cipher_suite = [0x13, 0x01]
    compression_method = [0x00]

    extensions = create_server_hello_extensions(keys)
    handshake = server_tls_version + server_random + [0x20] + [int(i) for i in session_id] + cipher_suite + compression_method + [int(i) for i in (len(extensions)).to_bytes(2, "big")] + extensions 

    handshake_data = [int(i) for i in (len(handshake) + 4).to_bytes(2, "big")]
    len_handshake = [int(i) for i in (len(handshake)).to_bytes(2, "big")]

    return ServerHello(handshake_record + protocol_version + handshake_data + [0x02, 0x00] + len_handshake + handshake, keys.private_key)


class Wrapper:
    def __init__(self, shs_key: bytes, shs_iv: bytes, chs_iv: bytes = None, chs_key: bytes = None):
        self.shs_key = shs_key
        self.shs_iv = shs_iv
        self.chs_key = chs_key
        self.chs_iv = chs_iv
        self.record_count = 0


    def wrap(self, data: bytes):
        handshake_record = bytes([0x17])
        protocol_version = bytes([0x03, 0x03])
        len_data_in_bytes = (len(data) + 17).to_bytes(2, "big")

        additional = handshake_record + protocol_version + len_data_in_bytes
        encrypted_data = utils.encrypt(self.shs_key, utils.xor_iv(self.shs_iv, self.record_count), data + bytes([0x16]), additional)
        
        record = additional + encrypted_data
        self.record_count += 1

        return record
   
