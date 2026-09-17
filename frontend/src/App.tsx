import { DocumentUpload } from "./components/DocumentUpload";
import { ChatPanel } from "./components/ChatPanel";
import { useDocuments } from "./hooks/useDocuments";
import "./styles/app.css";

export default function App() {
  const { documents, loading, refresh } = useDocuments();

  return (
    <div className="app-shell">
      <div className="app-bg" aria-hidden="true">
        <div className="app-bg-orb app-bg-orb--one" />
        <div className="app-bg-orb app-bg-orb--two" />
      </div>

      <div className="app">
        <header className="app-header">
          <div className="app-header-row">
            <div>
              <p className="app-eyebrow">Research assistant</p>
              <h1>AI Research Agent</h1>
              <p className="app-tagline">
                Search the web and get a clear summary — optionally grounded in your
                uploaded documents.
              </p>
              <ul className="feature-tags">
                <li>Web search</li>
                <li>Claude summaries</li>
                <li>Document RAG</li>
              </ul>
            </div>
            <span className="demo-badge">Demo</span>
          </div>
        </header>

        <main className="app-main">
          <DocumentUpload
            documents={documents}
            loading={loading}
            onDocumentsChange={refresh}
          />
          <ChatPanel hasDocuments={documents.length > 0} />
        </main>

        <footer className="app-footer">
          Tip: ask about your uploaded files with &ldquo;Include my documents&rdquo; checked.
        </footer>
      </div>
    </div>
  );
}
