from fastapi import FastAPI
from backend.app.api.upload import upload_router
from backend.app.services.query_test import query_router
from backend.app.api.rag import rag_router

app = FastAPI(title="Enterprise RAG API")
app.include_router(upload_router)
app.include_router(query_router)
app.include_router(rag_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Enterprise RAG API!"}