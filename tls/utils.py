import hashlib
import hmac
from collections import namedtuple
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, utils
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDFExpand
from cryptography.hazmat.primitives.serialization import Encoding, load_pem_private_key
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


def make_handshake_keys(client_public_key: X25519PublicKey, server_private_key: X25519PrivateKey, c_hello_msg: bytes, s_hello_msg: bytes):
    shared_secret = server_private_key.exchange(client_public_key)
    early_secret = hkdf_extract(b"\x00", b"\x00" * 32)

    hasher = hashlib.sha256()
    hasher.update(b"")
    empty_hash = hasher.digest()

    derived_secret = hkdf_expand_label(early_secret, b"derived", empty_hash, 32)
        
    handshake_secret = hkdf_extract(derived_secret, shared_secret)

    hasher = hashlib.sha256()
    hasher.update(c_hello_msg + s_hello_msg)
    hello_hash = hasher.digest()
    
    chs_secret = hkdf_expand_label(handshake_secret, b"c hs traffic", hello_hash, 32)
    shs_secret = hkdf_expand_label(handshake_secret, b"s hs traffic", hello_hash, 32)

    chs_key = hkdf_expand_label(chs_secret, b"key", b"", 16)
    shs_key = hkdf_expand_label(shs_secret, b"key", b"", 16)

    chs_iv = hkdf_expand_label(chs_secret, b"iv", b"", 12)
    shs_iv = hkdf_expand_label(shs_secret, b"iv", b"", 12)

    return HandshakeKeys(handshake_secret, chs_secret, chs_key, chs_iv, shs_secret, shs_key, shs_iv)


def hkdf_extract(salt: bytes, secret: bytes, hash=hashlib.sha256):
    return hmac.new(salt, secret, hash).digest()


def hkdf_expand_label(secret: bytes, label: bytes, context: bytes, length: int) -> bytes:
    label = b"tls13 " + label

    hkdf_label = (length.to_bytes(2, "big") + len(label).to_bytes(1, "big") + label + len(context).to_bytes(1, "big") + context)
    hkdf_expand = HKDFExpand(hashes.SHA256(), length, hkdf_label)
    
    return hkdf_expand.derive(secret)


def encrypt(key: bytes, iv: bytes, plaintext: bytes, additional: bytes = None) -> bytes:
    aesgcm = AESGCM(key)

    return aesgcm.encrypt(iv, plaintext, additional)


def decrypt(key: bytes, iv: bytes, ciphertext: bytes, additional: bytes):
    return AESGCM(key).decrypt(iv, ciphertext, additional)


def get_server_cert():
    with open("tls/server_cert.pem", "rb") as f:
        cert_data = f.read()
    
    cert = x509.load_pem_x509_certificate(cert_data)
    return cert.public_bytes(Encoding.DER)


def sign_hash(hashed_data: bytes):
    with open("tls/cert_priv_key.pem", "rb") as key_file:
        private_key = load_pem_private_key(
            key_file.read(),
            password=None
        )

    return private_key.sign(hashed_data, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=len(hashed_data)), utils.Prehashed(hashes.SHA256()))


def hash_messages(messages: bytes):
    hash = hashlib.sha256()
    hash.update(messages)

    return hash.digest()


def verify_data(shs_secret: bytes, msgs: bytes):
    finished_key = hkdf_expand_label(shs_secret, b"finished", b"", 32)
    hashed_msgs = hash_messages(msgs)

    hm = hmac.new(finished_key, hashed_msgs, hashlib.sha256)
    return hm.digest()


def make_server_app_keys(handshake_secret: bytes, msgs: bytes):
    derived_secret = hkdf_expand_label(handshake_secret, b"derived", hashlib.sha256(b"").digest(), 32)
    master_secret = hkdf_extract(derived_secret, None)
    hashed_msgs = hashlib.sha256(msgs).digest()

    client_secret = hkdf_expand_label(master_secret, b"s ap traffic", hashed_msgs, 32)
    server_secret = hkdf_expand_label(master_secret, b"s ap traffic", hashed_msgs, 32)

    client_app_key = hkdf_expand_label(client_secret, b"key", b"", 16)
    server_app_key = hkdf_expand_label(server_secret, b"key", b"", 16)

    client_app_iv = hkdf_expand_label(client_secret, b"key", b"", 12)
    server_app_iv = hkdf_expand_label(server_secret, b"iv", b"", 12)

    return client_app_key, client_app_iv, server_app_key, server_app_iv
