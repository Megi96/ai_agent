interface FormattedAnswerProps {
  text: string;
}

/** Render answer as clean paragraphs; strip noisy numbering Claude sometimes adds. */
export function FormattedAnswer({ text }: FormattedAnswerProps) {
  const cleaned = text
    .replace(/^\s*\d+\.\s+/gm, "")
    .replace(/^\s*[-*•]\s+/gm, "")
    .replace(/\[\d+\]/g, "")
    .trim();

  const paragraphs = cleaned.split(/\n\n+/).filter((p) => p.trim());

  if (paragraphs.length <= 1) {
    return <div className="answer-body">{cleaned}</div>;
  }

  return (
    <div className="answer-body">
      {paragraphs.map((paragraph, index) => (
        <p key={index} className="answer-paragraph">
          {paragraph.trim()}
        </p>
      ))}
    </div>
  );
}
