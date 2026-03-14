from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    message: str


class ContactResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str]
    message: str
    created_at: datetime

    model_config = {"from_attributes": True}
