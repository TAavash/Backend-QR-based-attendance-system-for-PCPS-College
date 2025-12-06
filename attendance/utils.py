from cryptography.fernet import Fernet

KEY = Fernet.generate_key()
cipher = Fernet(KEY)

def encrypt_token(text: str) -> str:
    return cipher.encrypt(text.encode()).decode()

def decrypt_token(token: str) -> str:
    return cipher.decrypt(token.encode()).decode()
