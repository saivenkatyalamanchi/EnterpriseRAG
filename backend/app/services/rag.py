from backend.app.services.retriever import retrieve
from backend.app.services.llm import generate


def answer_question(
    question: str
):
    chunks = retrieve(
        question
    )

    context = "\n\n".join(
        chunk["text"]
        for chunk in chunks
    )

    prompt = f"""
Answer ONLY using the provided context.

If the answer is not present,
say "I don't know."

Context:
{context}

Question:
{question}

Answer:
"""

    answer = generate(
        prompt
    )

    return {
        "answer": answer,
        "sources": chunks
    }