import os
from cryptography.fernet import Fernet
from math import radians, sin, cos, sqrt, atan2

# 1. PERSISTENT FERNET KEY (VERY IMPORTANT)

KEY_PATH = "fernet.key"   # stored in project root

# Load existing key or generate a new one
if os.path.exists(KEY_PATH):
    with open(KEY_PATH, "rb") as f:
        KEY = f.read()
else:
    KEY = Fernet.generate_key()
    with open(KEY_PATH, "wb") as f:
        f.write(KEY)

cipher = Fernet(KEY)

# 2. ENCRYPT / DECRYPT TOKEN

def encrypt_token(text: str) -> str:
    """Encrypts text using AES (Fernet) and returns a safe base64 string."""
    return cipher.encrypt(text.encode()).decode()


def decrypt_token(token: str) -> str:
    """Decrypts encrypted Fernet token. Raises exception if invalid."""
    return cipher.decrypt(token.encode()).decode()

# 3. DISTANCE CALCULATOR (Haversine formula)

def distance_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Returns distance between two lat/lng points in METERS.
    Uses Haversine great-circle formula.
    """
    R = 6371000  # Earth radius in meters

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        sin(dlat / 2) ** 2
        + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    )

    return R * 2 * atan2(sqrt(a), sqrt(1 - a))
