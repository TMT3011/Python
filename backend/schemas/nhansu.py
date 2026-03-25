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
class GeneralInfoNhanSu(BaseModel):
    id: int
    hoten: str
    email: EmailStr
    donvi: str
    image_data: Optional[str]
    class Config:
        form_attributes = True
