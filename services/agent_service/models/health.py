from pydantic import BaseModel

class HealthResponse(BaseModel):
    status: str
    agents_available: bool 