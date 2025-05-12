from collections import namedtuple
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from typing import List

KeyPair = namedtuple("KeyPair", ["private_key", "public_key"])


def generate_key_pair():
    private_key = X25519PrivateKey.generate()
    public_key = private_key.public_key()

    return KeyPair(private_key, public_key) 


def create_extension(id: int, contents: List[int]) -> List[int]:
    id_bytes = [int(i) for i in id.to_bytes(2, "big")]
    content_bytes = [int(i) for i in (len(contents)).to_bytes(2, "big")]
    extension = [*id_bytes, *content_bytes, *contents]
    print("extension ----> ", extension)

    return extension
