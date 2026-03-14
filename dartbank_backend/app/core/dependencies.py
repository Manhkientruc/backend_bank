# app/core/dependencies.py
from fastapi import Header, HTTPException
from app.core.security import verify_token

def get_current_user(authorization: str = Header(...)):

    token = authorization.replace("Bearer ", "")

    user_id = verify_token(token)

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user_id