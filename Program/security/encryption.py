from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

public_key = private_key.public_key()

def encrypt(data):
    byte_data = data.encode('utf-8')
    ciphertext = public_key.encrypt(
        byte_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        )
    )
    return ciphertext

def deterministic_encryption(data):
    byte_data = data.encode('utf-8')
    ciphertext = public_key.encrypt(
        byte_data,
        padding.PKCS1v15()  # Deterministic padding
    )
    return ciphertext

def decrypt(data):
    plaintext = private_key.decrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext.decode('utf-8')
