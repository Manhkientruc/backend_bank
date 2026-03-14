# app/schemas/user_schema.py
from pydantic import BaseModel

class UserRegister(BaseModel):
    full_name: str
    email: str
    phone: str
    citizen_id: str
    password: str