from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from database import get_db
from typing import List
from models.nhansu import NhanSu_Info, NhanSu_Image, GioiTinh, TrinhDo
from schemas.nhansu import DetailInfoNhanSu, GeneralInfoNhanSu
import base64
router = APIRouter()



#Lấy thông tin chi tiết của một nhân sự
@router.get("/detail_info", response_model=DetailInfoNhanSu)
async def get_detail_nhansu(
    id: int,
    db = Depends(get_db)
):
    async with db.cursor() as cur:
        try:
            sql = """
                SELECT hoten, email, gioitinh, trinhdo, donvi, hocham 
                FROM nhansu_info 
                WHERE id = %s
            """
            await cur.execute(sql, (id,))
            res = await cur.fetchone()
            if res:
                #Chuyển kết quả trả về thành Dictionary
                return {
                    "hoten": res[0],
                    "email": res[1],
                    "gioitinh": res[2],
                    "trinhdo": res[3],
                    "donvi": res[4],
                    "hocham": res[5]
                }
            else: 
                raise HTTPException(status_code=404, detail="Nhân sự không tồn tại")
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=400, detail=f"Lỗi hệ thống: {str(e)}")

#Lấy danh sách thông tin tong quat của một nhân sự
@router.get("/general_info", response_model=List[GeneralInfoNhanSu])
async def get_general_nhansu(db = Depends(get_db)):
    async with db.cursor() as cur:
        try:
            sql = "SELECT id, hoten, email, donvi, image_data FROM nhansu_info, nhansu_image WHERE nhansu_info.id = nhansu_image.nhansu_id;"
            await cur.execute(sql)
            rows = await cur.fetchall()
            
            if not rows:
                return []

            result = []
            for row in rows:
                binary_data = row[4]
                base64_str = None
                
                if binary_data:
                    encoded_string = base64.b64encode(binary_data).decode('utf-8')
                    base64_str = f"data:image/jpeg;base64,{encoded_string}"

                result.append({
                    "id": row[0],
                    "hoten": row[1],
                    "email": row[2],
                    "donvi": row[3],
                    "image_data": base64_str
                })
            
            return result

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")



#Tải lên thông tin nhân sự mới
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
            
            #Lấy ID nhân sự vừa được tạo
            person_id = cur.lastrowid

            #Chèn thông tin hình ảnh
            sql_img = "INSERT INTO nhansu_image (nhansu_id, filename, image_data) VALUES (%s, %s, %s)"
            await cur.execute(sql_img, (person_id, file.filename, image_bytes))

            await db.commit()
            
            return {"msg": "Đã thêm nhân sự và ảnh thành công", "id": person_id}
            
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=400, detail=f"Lỗi hệ thống: {str(e)}")
        
#Cập nhật thông tin nhân sự
@router.post("/update")
async def update_nhansu(
    id: int, 
    hoten: str = Form(...),
    email: str = Form(...),
    gioitinh: GioiTinh = Form(...),
    trinhdo: TrinhDo = Form(...),
    donvi: str = Form(...),
    hocham: str = Form(None),
    file: UploadFile = File(None), 
    db = Depends(get_db)
):
    async with db.cursor() as cur:
        try:
            #Kiểm tra nhân sự có tồn tại không
            await cur.execute("SELECT id FROM nhansu_info WHERE id = %s", (id,))
            if not await cur.fetchone():
                raise HTTPException(status_code=404, detail="Không tìm thấy nhân sự")

            #Cập nhật bảng nhansu_info
            sql_update_info = """
                UPDATE nhansu_info 
                SET hoten=%s, email=%s, gioitinh=%s, trinhdo=%s, donvi=%s, hocham=%s
                WHERE id=%s
            """
            await cur.execute(sql_update_info, (hoten, email, gioitinh.value, trinhdo.value, donvi, hocham, id))
            
            if file:
                image_bytes = await file.read()
                sql_update_img = """
                    UPDATE nhansu_image 
                    SET filename=%s, image_data=%s 
                    WHERE nhansu_id=%s
                """
                await cur.execute(sql_update_img, (file.filename, image_bytes, id))

            await db.commit()
            return {"msg": "Cập nhật nhân sự thành công", "id": id}

        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=400, detail=f"Lỗi cập nhật: {str(e)}")
        
#Xóa nhân sự
@router.delete("/delete")
async def delete_nhansu(
    id: int,
    db = Depends(get_db)
):
    async with db.cursor() as cur:
        try:
            #Kiểm tra nhân sự có tồn tại không
            await cur.execute("SELECT id FROM nhansu_info WHERE id = %s", (id,))
            if not await cur.fetchone():
                raise HTTPException(status_code=404, detail="Không tìm thấy nhân sự để xóa")
            sql = "DELETE FROM nhansu_info WHERE id = %s"
            await cur.execute(sql, (id,))
            await db.commit()
            return {"msg": f"Xóa nhân sự có ID {id} thành công"}
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=400, detail=f"Lỗi cập nhật: {str(e)}")