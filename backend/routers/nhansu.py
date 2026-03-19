from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from database import get_db
from models.nhansu import NhanSu_Info, NhanSu_Image, GioiTinh, TrinhDo
from schemas.nhansu import DetailInfoNhanSu

router = APIRouter()

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
            await cur.execute(sql_update_info, (hoten, email, gioitinh, trinhdo, donvi, hocham, id))
            
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