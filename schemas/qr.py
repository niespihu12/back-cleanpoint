from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class QRValidateRequest(BaseModel):
    user_id: int
    container_id: str
    photo: str  # Base64 encoded image

class QRValidateResponse(BaseModel):
    success: bool
    points_awarded: int
    new_balance: int
    message: Optional[str] = None

class QRTransaction(BaseModel):
    id: int
    user_id: int
    container_id: str
    image_url: str
    points_awarded: int
    validated: bool
    created_at: datetime

    class Config:
        orm_mode = True
