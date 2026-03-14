# app/routes/qr_routes.py
from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.services.account_service import get_my_account
from app.services.qr_service import generate_qr

router = APIRouter()

@router.get("/accounts/qr")
def account_qr(user_id: int = Depends(get_current_user)):

    account = get_my_account(user_id)

    return generate_qr(account["account_number"])