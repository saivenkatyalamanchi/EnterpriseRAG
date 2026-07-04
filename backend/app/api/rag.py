from fastapi import APIRouter

from backend.app.services.rag import (
    answer_question
)

rag_router = APIRouter(
    prefix="/rag",
    tags=["rag"]
)


@rag_router.post("/")
async def rag(
    question: str
):
    return answer_question(
        question
    )