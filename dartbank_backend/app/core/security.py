# app/core/security.py
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "dartbank_secret"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60

def create_token(user_id: int):

    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token


def verify_token(token: str):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["user_id"]
    except:
        return None