from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import padding
import hashlib
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

blocksize = 16

def customerEncrypt(message, string_key='password', salt='password'):
    key_bytes = string_key.encode()
    salt_bytes = salt.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt_bytes,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(key_bytes))
    cipher_suite = Fernet(key)
    encrypted_message = cipher_suite.encrypt(pad(message.encode(),blocksize))
    return encrypted_message.decode()

def customerDecrypt(encrypted_message, string_key='password', salt='password'):
    key_bytes = string_key.encode()
    salt_bytes = salt.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt_bytes,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(key_bytes))
    cipher_suite = Fernet(key)
    decrypted_message = cipher_suite.decrypt(encrypted_message.encode())
    return unpad(decrypted_message).decode()

def pad(data, block_size):
    # Calculate the number of bytes needed for padding
    padding_length = block_size - (len(data) % block_size) - 1
    # Padding byte with value 0x80
    padding = b'\x80'
    # Append zero bytes to complete the padding
    padding += b'\x00' * padding_length
    # Return the padded data
    return data + padding

def unpad(padded_data):

    # Find the position of the padding byte with value 0x80
    padding_index = padded_data.rfind(b'\x80')
    if padding_index == -1:
        raise ValueError("Invalid padding")
    # Extract the unpadded data
    unpadded_data = padded_data[:padding_index]
    return unpadded_data

def serverEncrypt(plaintext, public_key_string):
    public_key = serialization.load_pem_public_key(
        public_key_string.encode(),
        backend=default_backend()
    )
    ciphertext = public_key.encrypt(
        plaintext.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(ciphertext)

def serverDecrypt(ciphertext, private_key_string):
    private_key = serialization.load_pem_private_key(
        private_key_string.encode(),
        password=None,
        backend=default_backend()
    )
    ciphertext = base64.b64decode(ciphertext)
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext.decode()