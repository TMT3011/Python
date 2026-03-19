from fastapi import FastAPI
import aiomysql

app = FastAPI()

async def get_db():
    async with aiomysql.connect(
        host="localhost",
        user="root",
        password="",
        db="web_python"
    ) as db:
        yield db

