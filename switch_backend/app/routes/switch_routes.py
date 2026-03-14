# app/routes/switch_routes.py

from fastapi import APIRouter
from app.services.switch_service import process_interbank_transfer
from app.schemas.interbank_transfer import InterbankTransfer

router = APIRouter(
    prefix="/interbank",
    tags=["Interbank Transfer"]
)


@router.post("/transfer")
def interbank_transfer(data: InterbankTransfer):
    result = process_interbank_transfer(data.model_dump())
    return result