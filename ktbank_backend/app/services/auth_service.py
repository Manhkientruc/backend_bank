# app/services/auth_service.py
from app.core.database import get_db
from app.core.security import create_token

def login_user(data):

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT id, full_name, password_hash FROM users WHERE email=%s",
        (data.email,)
    )

    user = cursor.fetchone()

    conn.close()

    if not user:
        return {"error": "User not found"}

    if user["password_hash"] != data.password:
        return {"error": "Wrong password"}

    token = create_token(user["id"])

    return {
        "message": "Login successful",
        "token": token
    }