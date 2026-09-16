import { FormEvent, useEffect, useState } from "react";
import { checkHealth } from "../api/client";
import { useChat } from "../hooks/useChat";
import { MessageBubble } from "./MessageBubble";

const SAMPLE_TOPICS = [
  "Summarize the latest trends in AI agents",
  "What is retrieval-augmented generation (RAG)?",
  "What are the pros and cons of vector databases?",
];

interface ChatPanelProps {
  hasDocuments: boolean;
}

export function ChatPanel({ hasDocuments }: ChatPanelProps) {
  const { messages, loading, error, ask } = useChat();
  const [question, setQuestion] = useState("");
  const [includeDocs, setIncludeDocs] = useState(true);
  const [apiOnline, setApiOnline] = useState<boolean | null>(null);

  useEffect(() => {
    checkHealth()
      .then(() => setApiOnline(true))
      .catch(() => setApiOnline(false));
  }, []);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const trimmed = question.trim();
    if (!trimmed || loading) return;
    setQuestion("");
    await ask(trimmed, true, includeDocs);
  }

  async function handleSampleQuestion(sample: string) {
    if (loading) return;
    setQuestion("");
    await ask(sample, true, includeDocs);
  }

  return (
    <section className="panel chat-panel">
      <div className="chat-panel-header">
        <h2>Search &amp; summarize</h2>
        <span
          className={`status-pill ${apiOnline === false ? "status-pill--offline" : "status-pill--online"}`}
        >
          {apiOnline === null ? "Checking API..." : apiOnline ? "API online" : "API offline"}
        </span>
      </div>

      <div className="messages">
        {messages.length === 0 && (
          <p className="empty-state">
            Enter a topic — the agent searches the web and writes a summary.
            {hasDocuments && includeDocs
              ? " Your uploaded documents are included as extra context."
              : ""}
          </p>
        )}
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}
      </div>

      {messages.length === 0 && (
        <div className="sample-questions">
          <p className="sample-questions-label">Try a topic:</p>
          <div className="sample-questions-list">
            {SAMPLE_TOPICS.map((sample) => (
              <button
                key={sample}
                type="button"
                className="sample-question"
                onClick={() => handleSampleQuestion(sample)}
                disabled={loading || apiOnline === false}
              >
                {sample}
              </button>
            ))}
          </div>
        </div>
      )}

      {error && <p className="error">{error}</p>}

      <form className="chat-form" onSubmit={handleSubmit}>
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="e.g. Summarize recent news about quantum computing"
          rows={3}
          disabled={apiOnline === false}
        />
        <div className="chat-form-actions">
          {hasDocuments ? (
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={includeDocs}
                onChange={(e) => setIncludeDocs(e.target.checked)}
              />
              Include my documents
            </label>
          ) : (
            <span className="checkbox-label">Web search enabled</span>
          )}
          <button
            type="submit"
            disabled={loading || !question.trim() || apiOnline === false}
          >
            {loading ? "Searching..." : "Summarize"}
          </button>
        </div>
      </form>
    </section>
  );
}
