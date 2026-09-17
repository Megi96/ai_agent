import { ChangeEvent, useState } from "react";
import {
  DocumentMetadata,
  seedDemoDocuments,
  uploadDocument,
} from "../api/client";
import { DocumentList } from "./DocumentList";

interface DocumentUploadProps {
  documents: DocumentMetadata[];
  loading: boolean;
  onDocumentsChange: () => Promise<void>;
}

export function DocumentUpload({
  documents,
  loading,
  onDocumentsChange,
}: DocumentUploadProps) {
  const [status, setStatus] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function handleFileChange(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) return;

    setBusy(true);
    setStatus(null);
    try {
      const response = await uploadDocument(file);
      setStatus(`Uploaded: ${response.document.filename}`);
      await onDocumentsChange();
    } catch (err) {
      setStatus(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setBusy(false);
      event.target.value = "";
    }
  }

  async function handleLoadDemo() {
    setBusy(true);
    setStatus(null);
    try {
      const response = await seedDemoDocuments();
      setStatus(response.message);
      await onDocumentsChange();
    } catch (err) {
      setStatus(err instanceof Error ? err.message : "Demo load failed");
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="panel upload-panel">
      <h2>Documents</h2>
      <p className="panel-description">
        Upload PDF, DOCX, TXT, or Markdown — or load the bundled demo set to try
        a question right away.
      </p>

      <button
        type="button"
        className="demo-button"
        onClick={handleLoadDemo}
        disabled={busy}
      >
        {busy ? "Working..." : "Load demo documents"}
      </button>

      <label className="upload-zone">
        <input
          type="file"
          accept=".pdf,.docx,.txt,.md,.markdown"
          onChange={handleFileChange}
          disabled={busy}
        />
        <span className="upload-zone-icon" aria-hidden="true">
          ↑
        </span>
        <span className="upload-zone-text">
          {busy ? "Please wait..." : "Drop a file here or click to browse"}
        </span>
        <span className="upload-zone-hint">PDF, DOCX, TXT, Markdown</span>
      </label>

      {status && (
        <p className={status.toLowerCase().includes("fail") ? "error" : "upload-status"}>
          {status}
        </p>
      )}

      <DocumentList documents={documents} loading={loading} />
    </section>
  );
}
