from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="RetailMind AI Backend",
    description="Smart Retail Assistant APIs",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
def home():
    return {"message": "RetailMind AI Backend is running"}