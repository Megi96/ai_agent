from langchain_core.embeddings import Embeddings


def get_embeddings() -> Embeddings:
    """Return the embedding model for document vectorization."""
    # TODO: wire Anthropic or sentence-transformers embeddings
    from langchain_community.embeddings import FakeEmbeddings

    return FakeEmbeddings(size=384)
