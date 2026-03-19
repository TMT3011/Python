from pydantic import BaseModel, EmailStr
from typing import Optional

class DetailInfoNhanSu(BaseModel):
    hoten: str
    email: EmailStr
    gioitinh: str
    trinhdo: str
    donvi: str
    hocham: Optional[str]
    class Config:
        form_attributes = True