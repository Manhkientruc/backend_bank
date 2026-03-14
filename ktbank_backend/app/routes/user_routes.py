# app/routes/user_routes.py
from fastapi import APIRouter
from app.services.user_service import fetch_users, register_user
from app.schemas.user_schema import UserRegister

router = APIRouter()

@router.get("/users")
def get_users():
    return fetch_users()

@router.post("/users/register")
def create_user(data: UserRegister):
    return register_user(data)