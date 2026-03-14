# app/routes/transaction_routes.py
from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.services.transaction_service import get_transactions

router = APIRouter()

@router.get("/transactions")
def transactions(user_id: int = Depends(get_current_user)):
    return get_transactions(user_id)