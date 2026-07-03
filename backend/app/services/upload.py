from fastapi import APIRouter

upload_router = APIRouter(prefix="/upload")

@upload_router.get("/")
async def upload_root():
    return {"message": "Welcome to the Upload Service!"}

