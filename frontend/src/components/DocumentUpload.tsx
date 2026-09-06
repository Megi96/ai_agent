import { ChangeEvent, useState } from "react";
import { uploadDocument } from "../api/client";

export function DocumentUpload() {
  const [status, setStatus] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);

  async function handleFileChange(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) return;

    setUploading(true);
    setStatus(null);
    try {
      const response = await uploadDocument(file);
      setStatus(`Uploaded: ${response.document.filename}`);
    } catch (err) {
      setStatus(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setUploading(false);
      event.target.value = "";
    }
  }

  return (
    <section className="panel upload-panel">
      <h2>Documents</h2>
      <p className="panel-description">
        Upload PDF, DOCX, TXT, or Markdown files to build your knowledge base.
      </p>
      <label className="upload-zone">
        <input
          type="file"
          accept=".pdf,.docx,.txt,.md,.markdown"
          onChange={handleFileChange}
          disabled={uploading}
        />
        <span>{uploading ? "Uploading..." : "Choose a file or drop it here"}</span>
      </label>
      {status && <p className="upload-status">{status}</p>}
    </section>
  );
}
