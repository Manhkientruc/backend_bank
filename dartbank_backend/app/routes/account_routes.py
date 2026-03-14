# app/routes/account_routes.py
from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.services.account_service import get_my_account

router = APIRouter()

@router.get("/accounts/me")
def my_account(user_id: int = Depends(get_current_user)):
    return get_my_account(user_id)