from app.models.chat import Source, SourceType
from app.config import settings
from app.rag.vectorstore import get_vectorstore


async def retrieve_documents(query: str, top_k: int | None = None) -> list[Source]:
    """Retrieve relevant document chunks from the vector store."""
    limit = top_k or settings.retrieval_top_k
    vectorstore = get_vectorstore()
    results = vectorstore.similarity_search(query, k=limit)

    sources: list[Source] = []
    for doc in results:
        filename = doc.metadata.get("filename", "Unknown document")
        document_id = doc.metadata.get("document_id")
        page = doc.metadata.get("page")
        title = f"{filename}" + (f" (page {page})" if page else "")
        snippet = doc.page_content.strip()
        if len(snippet) > 300:
            snippet = snippet[:297] + "..."

        sources.append(
            Source(
                type=SourceType.DOCUMENT,
                title=title,
                snippet=snippet,
                document_id=document_id,
            )
        )

    return sources
