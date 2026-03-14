# app/schemas/transfer_schema.py
from pydantic import BaseModel

class TransferRequest(BaseModel):
    from_account: str
    to_account: str
    to_bank: str
    amount: float