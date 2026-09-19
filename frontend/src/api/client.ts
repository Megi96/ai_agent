export interface Source {
  type: "document" | "web";
  title: string;
  snippet: string;
  url?: string | null;
  document_id?: string | null;
}

export interface ChatResponse {
  answer: string;
  sources: Source[];
}

export interface DocumentMetadata {
  id: string;
  filename: string;
  content_type: string;
  size_bytes: number;
  chunk_count: number;
  ingested_at: string;
}

export interface UploadResponse {
  document: DocumentMetadata;
  message: string;
}

/** Dev: Vite proxies `/api` → backend. Production: set VITE_API_URL to your Render URL. */
const API_BASE = (import.meta.env.VITE_API_URL as string | undefined)?.replace(
  /\/$/,
  ""
) ?? "/api";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, options);
  if (!response.ok) {
    const text = await response.text();
    try {
      const json = JSON.parse(text) as { detail?: string };
      if (json.detail) throw new Error(json.detail);
    } catch {
      /* not JSON */
    }
    throw new Error(
      response.status === 500
        ? "Server error — check that ANTHROPIC_API_KEY is valid in .env and restart the backend."
        : text || `Request failed: ${response.status}`
    );
  }
  return response.json() as Promise<T>;
}

export async function checkHealth(): Promise<{ status: string }> {
  return request("/health");
}

export async function uploadDocument(file: File): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append("file", file);
  return request("/documents/upload", { method: "POST", body: formData });
}

export async function listDocuments(): Promise<DocumentMetadata[]> {
  return request("/documents");
}

export interface SeedDemoResponse {
  message: string;
  count: number;
  documents: DocumentMetadata[];
}

export async function seedDemoDocuments(): Promise<SeedDemoResponse> {
  return request("/demo/seed", { method: "POST" });
}

export async function sendChat(
  question: string,
  useWeb: boolean,
  useDocuments: boolean = true
): Promise<ChatResponse> {
  return request("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      question,
      use_web: useWeb,
      use_documents: useDocuments,
    }),
  });
}
