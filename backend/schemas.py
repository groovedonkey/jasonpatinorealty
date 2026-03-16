from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    business_name: Optional[str] = None
    phone: str
    email: EmailStr
    interest: str
    message: Optional[str] = None


class ContactResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    business_name: Optional[str]
    phone: str
    email: str
    interest: str
    message: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}
