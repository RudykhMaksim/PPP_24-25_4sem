import logging
import uvicorn
from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.encode import router as encode_router
from datetime import datetime
import pytz

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(encode_router, prefix="/encode")

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Время старта сервера
start_time = datetime.now(pytz.timezone("Europe/Paris")).strftime("%I:%M %p %Z, %A, %B %d, %Y")

@app.on_event("startup")
async def startup_event():
    logger.info("Starting FastAPI server with WebSocket...")

@app.get("/")
async def root():
    return {"message": f"Welcome to Encryption API - Started at {start_time}"}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )