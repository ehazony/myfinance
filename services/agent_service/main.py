# Import config to load all environment variables
import config

from fastapi import FastAPI
from api.chat import router as chat_router
from api.health import router as health_router

app = FastAPI(title="Agent Service API", version="1.0.0")

app.include_router(chat_router, prefix="/api/chat")
app.include_router(health_router, prefix="/api/health") 