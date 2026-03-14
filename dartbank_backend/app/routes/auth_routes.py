# app/routes/auth_routes.py
from fastapi import APIRouter
from app.schemas.auth_schema import LoginRequest
from app.services.auth_service import login_user

router = APIRouter()

@router.post("/auth/login")
def login(data: LoginRequest):
    return login_user(data)