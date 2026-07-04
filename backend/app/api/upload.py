import uuid
from fastapi import APIRouter, File, UploadFile, HTTPException, status
import aiofiles
from pathlib import Path
from backend.app.services.parser import parse_pdf

upload_router = APIRouter(prefix="/upload")

@upload_router.get("/")
async def upload_root():
    return {"message": "Welcome to the Upload Service!"}

@upload_router.post("/file")
async def upload_file(file: UploadFile = File(...)):
    # File processing logic goes here
    ALLOWED_MIME_TYPES = {
        "application/pdf",
        "text/plain",
    }
    
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Unsupported file type. Allowed types: {ALLOWED_MIME_TYPES}"
        )
    
    SAVE_DIR = Path(__file__).resolve().parents[2] / "data" / "uploads"
    SAVE_DIR.mkdir(exist_ok=True)
    
    saved_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = SAVE_DIR / saved_filename
    try:
        async with aiofiles.open(file_path, 'wb') as out_file:
            while content := await file.read(1024 * 1024):  # Read file in chunks
                await out_file.write(content)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while saving the file: {str(e)}"
        )
    finally:
        await file.close()
    
    documents = parse_pdf(file_path)
    
    return {"filename": saved_filename, "message": "File uploaded successfully.", "documents": documents}
            
    
    
    
