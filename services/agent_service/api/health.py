from fastapi import APIRouter
from models.health import HealthResponse

router = APIRouter()

@router.get("/", response_model=HealthResponse)
def health():
    return HealthResponse(status="ok", agents_available=True) 