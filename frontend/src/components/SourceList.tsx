import { Source } from "../api/client";

interface SourceListProps {
  sources: Source[];
}

export function SourceList({ sources }: SourceListProps) {
  if (sources.length === 0) return null;

  return (
    <div className="source-list">
      <p className="source-list-title">Sources</p>
      <ul>
        {sources.map((source, index) => (
          <li key={`${source.title}-${index}`} className="source-item">
            <span className={`source-badge source-badge--${source.type}`}>
              {source.type}
            </span>
            {source.url ? (
              <a href={source.url} target="_blank" rel="noreferrer">
                {source.title}
              </a>
            ) : (
              <span>{source.title}</span>
            )}
            <p className="source-snippet">{source.snippet}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
