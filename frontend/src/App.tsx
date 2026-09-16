import { DocumentUpload } from "./components/DocumentUpload";
import { ChatPanel } from "./components/ChatPanel";
import { useDocuments } from "./hooks/useDocuments";
import "./styles/app.css";

export default function App() {
  const { documents, loading, refresh } = useDocuments();

  return (
    <div className="app">
      <header className="app-header">
        <div className="app-header-row">
          <div>
            <h1>AI Research Agent</h1>
            <p>Search the web and get a summarized answer — with optional document context.</p>
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
    </div>
  );
}
