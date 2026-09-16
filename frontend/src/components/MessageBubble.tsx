import { Message } from "../hooks/useChat";
import { FormattedAnswer } from "./FormattedAnswer";
import { SourceList } from "./SourceList";

interface MessageBubbleProps {
  message: Message;
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user";

  return (
    <div className={`message message--${message.role}`}>
      <div className="message-header">
        <span className="message-avatar">{isUser ? "You" : "AI"}</span>
        <span className="message-label">{isUser ? "Your question" : "Summary"}</span>
      </div>
      {isUser ? (
        <p className="message-content">{message.content}</p>
      ) : (
        <FormattedAnswer text={message.content} />
      )}
      {message.sources && message.role === "assistant" && (
        <SourceList sources={message.sources} />
      )}
    </div>
  );
}
