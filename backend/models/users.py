from sqlmodel import SQLModel, Field
from pydantic import EmailStr

class Users(SQLModel, table=True):
    email: EmailStr = Field(primary_key=True, max_length=255)
    name: str = Field(nullable=False)
    matkhau: str = Field(nullable=False)
