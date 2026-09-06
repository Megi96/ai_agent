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

const API_BASE = "/api";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, options);
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed: ${response.status}`);
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

export async function sendChat(
  question: string,
  useWeb: boolean
): Promise<ChatResponse> {
  return request("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, use_web: useWeb }),
  });
}
