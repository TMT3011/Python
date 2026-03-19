from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.user import router as user_router
from routers.nhansu import router as nhansu_router

app = FastAPI()
# origins = [
#     "http://localhost:5173",
#     "http://localhost:5174"
# ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/user")
app.include_router(nhansu_router, prefix="/nhansu")