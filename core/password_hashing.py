from cryptography.fernet import Fernet
import base64

# Initialize the Fernet cipher with the provided key
fernet = Fernet()

def encrypt_data(plain_data: str) -> str:
    data_bytes = plain_data.encode("utf-8")
    encrypted_plain_data = fernet.encrypt(data_bytes)
    return base64.b64encode(encrypted_plain_data).decode("utf-8")

def decrypt_data(encoded_data: str) -> str:
    encrypted_data = base64.b64decode(encoded_data)
    decrypted_data = fernet.decrypt(encrypted_data)
    return decrypted_data.decode("utf-8")
