# app/schemas/interbank_transfer.py

from pydantic import BaseModel


class InterbankTransfer(BaseModel):
    from_bank: str
    to_bank: str
    from_account: str
    to_account: str
    amount: float