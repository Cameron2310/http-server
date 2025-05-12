from collections import namedtuple
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey

KeyPair = namedtuple("KeyPair", ["private_key", "public_key"])


def generate_key_pair():
    private_key = X25519PrivateKey.generate()
    public_key = private_key.public_key()

    return KeyPair(private_key, public_key) 
