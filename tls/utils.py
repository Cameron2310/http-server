import hashlib
import hmac
from collections import namedtuple
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDFExpand
from cryptography.hazmat.primitives.serialization import Encoding
from typing import List


KeyPair = namedtuple("KeyPair", ["private_key", "public_key"])
HandshakeKeys = namedtuple("HandshakeKeys", ["handshake_secret", "chs", "chs_key", "chs_iv", "shs", "shs_key", "shs_iv"])


def generate_public_key(key: bytes):
    return X25519PublicKey.from_public_bytes(key)


def generate_key_pair():
    private_key = X25519PrivateKey.generate()
    public_key = private_key.public_key()

    return KeyPair(private_key, public_key) 


def create_extension(id: int, contents) -> List[int]:
    id_bytes = [int(i) for i in id.to_bytes(2, "big")]
    content_bytes = [int(i) for i in (len(contents)).to_bytes(2, "big")]

    return [*id_bytes, *content_bytes, *contents]


def make_handshake_keys(client_public_key: X25519PublicKey, server_private_key: X25519PrivateKey, s_hello_msg: bytes, c_hello_msg: bytes):
    shared_secret = server_private_key.exchange(client_public_key)
    early_secret = hkdf_extract(hashlib.sha384, bytes(32), bytes(32))
    derived_secret = derive_secret(early_secret, "derived", bytes())
        
    handshake_secret = hkdf_extract(hashlib.sha384, shared_secret, derived_secret)
    
    chs_secret = derive_secret(handshake_secret, "c hs traffic", c_hello_msg + s_hello_msg)
    chs_key = hkdf_expand_label(chs_secret, "key", bytes(), 16)
    chs_iv = hkdf_expand_label(chs_secret, "iv", bytes(), 12)

    shs_secret = derive_secret(handshake_secret, "s hs traffic", c_hello_msg + s_hello_msg)
    shs_key = hkdf_expand_label(shs_secret, "key", bytes(), 16)
    shs_iv = hkdf_expand_label(shs_secret, "iv", bytes(), 12)

    return HandshakeKeys(handshake_secret, chs_secret, chs_key, chs_iv, shs_secret, shs_key, shs_iv)


def hkdf_extract(hash, secret: bytes, salt: bytes):
    return hmac.new(salt, secret, hash).digest()


def derive_secret(secret: bytes, label: str, context: bytes) -> bytes:
    hash = hashlib.sha384(context).digest()

    return hkdf_expand_label(secret, label, hash, 32)


def hkdf_expand_label(secret: bytes, label: str, context: bytes, length: int) -> bytes:
    hkdf_label = bytes()
    hkdf_label += length.to_bytes(2, "big")

    hkdf_label += b'tls13 '
    hkdf_label += bytes(label, "utf-8")
    hkdf_label += context

    hkdf_expand = HKDFExpand(hashes.SHA384(), length, hkdf_label)
    key = hkdf_expand.derive(secret)

    return key


def encrypt(key: bytes, iv: bytes, plaintext: bytes, additional: bytes = None) -> bytes:
    aesgcm = AESGCM(key)

    return aesgcm.encrypt(iv, plaintext, additional)


def get_server_cert():
    with open("tls/server.crt", "rb") as f:
        cert_data = f.read()
    
    cert = x509.load_pem_x509_certificate(cert_data)
    return cert.public_bytes(Encoding.DER)
