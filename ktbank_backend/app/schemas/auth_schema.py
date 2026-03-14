# app/schemas/auth_schema.py
from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str