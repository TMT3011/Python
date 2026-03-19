from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from database import get_db
from models.nhansu import NhanSu_Info, NhanSu_Image, GioiTinh, TrinhDo

router = APIRouter()

@router.post("/upload")
async def upload_nhansu(
    hoten: str = Form(...),
    email: str = Form(...),
    gioitinh: GioiTinh = Form(...),
    trinhdo: TrinhDo = Form(...),
    donvi: str = Form(...),
    hocham: str = Form(None),
    file: UploadFile = File(...),
    db = Depends(get_db)
):
    image_bytes = await file.read()
    async with db.cursor() as cur:
        try:
            # Chèn thông tin nhân sự
            sql_nhansu = """
                INSERT INTO nhansu_info (hoten, email, gioitinh, trinhdo, donvi, hocham) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            await cur.execute(sql_nhansu, (hoten, email, gioitinh, trinhdo, donvi, hocham))
            
            #Lấy ID vừa nhân sự vừa được tạo
            person_id = cur.lastrowid

            #Chèn thông tin hình ảnh
            sql_img = "INSERT INTO nhansu_image (nhansu_id, filename, image_data) VALUES (%s, %s, %s)"
            await cur.execute(sql_img, (person_id, file.filename, image_bytes))

            await db.commit()
            
            return {"msg": "Đã thêm nhân sự và ảnh thành công", "id": person_id}
            
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=400, detail=f"Lỗi hệ thống: {str(e)}")