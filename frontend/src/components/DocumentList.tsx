import { DocumentMetadata } from "../api/client";

interface DocumentListProps {
  documents: DocumentMetadata[];
  loading: boolean;
}

export function DocumentList({ documents, loading }: DocumentListProps) {
  if (loading) {
    return <p className="doc-list-empty">Loading documents...</p>;
  }

  if (documents.length === 0) {
    return (
      <p className="doc-list-empty">
        No documents yet. Upload a file or load the demo set.
      </p>
    );
  }

  return (
    <ul className="doc-list">
      {documents.map((doc) => (
        <li key={doc.id} className="doc-list-item">
          <span className="doc-list-name">{doc.filename}</span>
          <span className="doc-list-meta">
            {doc.chunk_count} chunk{doc.chunk_count === 1 ? "" : "s"}
          </span>
        </li>
      ))}
    </ul>
  );
}
