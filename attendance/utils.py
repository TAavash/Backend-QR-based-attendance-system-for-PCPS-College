from cryptography.fernet import Fernet
from math import radians, sin, cos, sqrt, atan2

KEY = Fernet.generate_key()
cipher = Fernet(KEY)

def encrypt_token(text: str) -> str:
    return cipher.encrypt(text.encode()).decode()

def decrypt_token(token: str) -> str:
    return cipher.decrypt(token.encode()).decode()

def distance_m(lat1, lon1, lat2, lon2):
    R = 6371000
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1-a))
