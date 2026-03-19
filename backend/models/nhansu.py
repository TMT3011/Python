from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr
from enum import Enum
from typing import Optional

class GioiTinh(str, Enum):
    male="male"
    female="female"
class TrinhDo(str, Enum):
    thacsi="thacsi"
    tiensi="tiensi"
    phogiaosu="phogiaosu"
    giaosu="giaosu"

class NhanSu_Info(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    hoten: str = Field(nullable=False, max_length=255)
    email: EmailStr = Field(nullable=False, unique=True, max_length=255)
    gioitinh: GioiTinh = Field(nullable=False)
    trinhdo: TrinhDo = Field(nullable=False)
    donvi: str = Field(nullable=False, max_length=255)
    hocham: Optional[str] = Field(default=None, max_length=255)

    #Thuộc tính quan hệ 1-1 với NhanSu_Image
    hinhanh: Optional["NhanSu_Image"] = Relationship(
        back_populates="nhansu",
        sa_relationship_kwargs={"uselist": False} #Chỉ lưu quan hệ với một đối tượng chứ không phải danh sách
    )
class NhanSu_Image(SQLModel, table=True):
    image_id: int = Field(primary_key=True)
    nhansu_id: int = Field(
        foreign_key="nhansu_info.id", 
        unique=True, 
        ondelete="CASCADE"
    )
    file_name: str = Field(nullable=False, max_length=255)
    image_data: bytes

    #Thuộc tính quan hệ 1-1 với NhanSu_Info
    nhansu: Optional[NhanSu_Info] = Relationship(back_populates="hinhanh")