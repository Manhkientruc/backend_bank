# app/main.py
from fastapi import FastAPI
from app.routes.user_routes import router as user_router
from app.routes.transfer_routes import router as transfer_router
from app.routes.auth_routes import router as auth_router
from app.routes.account_routes import router as account_router
from app.routes.transaction_routes import router as transaction_router
from app.routes.qr_routes import router as qr_router
from app.routes.interbank_routes import router as interbank_router

app = FastAPI()

app.include_router(user_router)
app.include_router(transfer_router)
app.include_router(auth_router)
app.include_router(account_router)
app.include_router(transaction_router)
app.include_router(qr_router)
app.include_router(interbank_router)

@app.get("/")
def root():
    return {"message": "DartBank API running"}