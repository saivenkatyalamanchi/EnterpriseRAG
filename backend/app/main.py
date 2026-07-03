from fastapi import FastAPI
from services.upload import upload_router

app = FastAPI(title="Enterprise RAG API")
app.include_router(upload_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Enterprise RAG API!"}