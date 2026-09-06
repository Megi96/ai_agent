from app.models.chat import Source


async def retrieve_documents(query: str, top_k: int = 5) -> list[Source]:
    """Retrieve relevant document chunks from the vector store."""
    # TODO: implement ChromaDB similarity search
    _ = query, top_k
    return []
