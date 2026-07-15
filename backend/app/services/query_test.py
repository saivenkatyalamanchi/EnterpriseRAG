from fastapi import APIRouter
from backend.app.services.retriever import hybrid_retrieve

query_router = APIRouter(
    prefix="/query",
    tags=["query"]
)


@query_router.post("/")
async def query(
    question: str
):
    return hybrid_retrieve(question)