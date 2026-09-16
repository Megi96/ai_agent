# AI Research Agent — Demo Notes

This is sample demo content for trying the RAG pipeline.

## What this project does

The AI Research Agent ingests documents, stores them in a vector database (ChromaDB),
and retrieves relevant passages when you ask a question.

## Key concepts

- **RAG (Retrieval-Augmented Generation):** Search your docs first, then answer using that context.
- **Embeddings:** Text is converted to vectors so similar meaning can be found semantically.
- **Chunking:** Long documents are split into smaller pieces before indexing.

## Sample facts for testing

- The default embedding model is `all-MiniLM-L6-v2`.
- Supported upload formats include PDF, DOCX, TXT, and Markdown.
- The backend API runs on port 8000 by default.
- The demo UI runs on port 5173 via Vite.

Try asking: "What embedding model does this project use?" or "Which file formats are supported?"
