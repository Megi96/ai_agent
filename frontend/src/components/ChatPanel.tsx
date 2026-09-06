import { FormEvent, useState } from "react";
import { useChat } from "../hooks/useChat";
import { MessageBubble } from "./MessageBubble";

export function ChatPanel() {
  const { messages, loading, error, ask } = useChat();
  const [question, setQuestion] = useState("");
  const [useWeb, setUseWeb] = useState(false);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const trimmed = question.trim();
    if (!trimmed || loading) return;
    setQuestion("");
    await ask(trimmed, useWeb);
  }

  return (
    <section className="panel chat-panel">
      <h2>Ask a question</h2>
      <div className="messages">
        {messages.length === 0 && (
          <p className="empty-state">
            Upload documents, then ask questions about them.
          </p>
        )}
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}
      </div>
      {error && <p className="error">{error}</p>}
      <form className="chat-form" onSubmit={handleSubmit}>
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="What would you like to know?"
          rows={3}
        />
        <div className="chat-form-actions">
          <label className="checkbox-label">
            <input
              type="checkbox"
              checked={useWeb}
              onChange={(e) => setUseWeb(e.target.checked)}
            />
            Search web
          </label>
          <button type="submit" disabled={loading || !question.trim()}>
            {loading ? "Thinking..." : "Send"}
          </button>
        </div>
      </form>
    </section>
  );
}
