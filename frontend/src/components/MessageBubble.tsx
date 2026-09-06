import { Message } from "../hooks/useChat";
import { SourceList } from "./SourceList";

interface MessageBubbleProps {
  message: Message;
}

export function MessageBubble({ message }: MessageBubbleProps) {
  return (
    <div className={`message message--${message.role}`}>
      <p className="message-role">{message.role === "user" ? "You" : "Agent"}</p>
      <p className="message-content">{message.content}</p>
      {message.sources && message.role === "assistant" && (
        <SourceList sources={message.sources} />
      )}
    </div>
  );
}
