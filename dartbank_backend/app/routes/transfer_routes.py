# app/routes/transfer_routes.py
from fastapi import APIRouter, Depends
from app.schemas.transfer_schema import TransferRequest
from app.services.transfer_service import transfer_money
from app.core.dependencies import get_current_user

router = APIRouter()

@router.post("/transfer")
def transfer(
    data: TransferRequest,
    user_id: int = Depends(get_current_user)
):
    return transfer_money(data, user_id)