# app/main.py

from fastapi import FastAPI
from app.routes.switch_routes import router as switch_router

app = FastAPI(
    title="Switch Service",
    description="Interbank Switch for DartBank, KtBank, JavaBank",
    version="1.0.0"
)

app.include_router(switch_router)

@app.get("/")
def root():
    return {"message": "Switch Service Running"}
