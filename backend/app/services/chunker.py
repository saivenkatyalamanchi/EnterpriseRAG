from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    separators=["\n\n", "\n", " ", ""]
)

def chunk_documents(documents):
    chunked_documents = []

    for document in documents:
        content = document["content"]
        metadata = document["metadata"]

        chunks = splitter.split_text(content)

        for i, chunk in enumerate(chunks):
            chunked_documents.append(
                {
                    "chunk": chunk,
                    "metadata": {
                        **metadata,
                        "chunk_index": i + 1,
                        "total_chunks": len(chunks)
                    }
                }
            )

    return chunked_documents