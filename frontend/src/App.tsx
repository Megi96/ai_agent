import { DocumentUpload } from "./components/DocumentUpload";
import { ChatPanel } from "./components/ChatPanel";
import "./styles/app.css";

export default function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>AI Research Agent</h1>
        <p>Ingest documents, ask questions, search the web.</p>
      </header>
      <main className="app-main">
        <DocumentUpload />
        <ChatPanel />
      </main>
    </div>
  );
}
