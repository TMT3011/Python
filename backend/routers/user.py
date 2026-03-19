from fastapi import APIRouter, Depends, HTTPException
from models.users import Users
from database import get_db

router = APIRouter()

@router.post("/login")
async def login(
    user: Users,
    db = Depends(get_db)
):
    async with db.cursor() as cur:
        query = "SELECT * FROM users WHERE email=%s AND matkhau=%s"
        await cur.execute(query, (user.email, user.matkhau)) 
        res = await cur.fetchone()
        if res:
            return {"status": "success"}
        else:
            raise HTTPException(status_code=401, detail="Email hoặc mật khẩu không đúng")