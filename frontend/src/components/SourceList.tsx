import { useState } from "react";
import { Source } from "../api/client";

interface SourceListProps {
  sources: Source[];
}

const MAX_VISIBLE = 4;

export function SourceList({ sources }: SourceListProps) {
  const [expanded, setExpanded] = useState(false);

  if (sources.length === 0) return null;

  const visible = expanded ? sources : sources.slice(0, MAX_VISIBLE);
  const hiddenCount = sources.length - MAX_VISIBLE;

  return (
    <details className="source-list" open>
      <summary className="source-list-toggle">
        Sources ({sources.length})
      </summary>
      <ul className="source-chips">
        {visible.map((source, index) => (
          <li key={`${source.title}-${index}`} className="source-chip">
            <span className={`source-badge source-badge--${source.type}`}>
              {source.type === "web" ? "Web" : "Doc"}
            </span>
            {source.url ? (
              <a href={source.url} target="_blank" rel="noreferrer" title={source.snippet}>
                {source.title}
              </a>
            ) : (
              <span title={source.snippet}>{source.title}</span>
            )}
          </li>
        ))}
      </ul>
      {hiddenCount > 0 && !expanded && (
        <button
          type="button"
          className="source-show-more"
          onClick={() => setExpanded(true)}
        >
          Show {hiddenCount} more
        </button>
      )}
    </details>
  );
}
