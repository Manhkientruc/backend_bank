# app/schemas/transfer_schema.py
from pydantic import BaseModel

class TransferRequest(BaseModel):
    from_account: str
    to_bank: str
    to_account: str
    amount: float