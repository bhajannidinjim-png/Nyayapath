import { UploadCloud } from "lucide-react";
import { useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import WorkflowTracker from "../components/WorkflowTracker.jsx";
import { uploadJudgment } from "../services/api.js";

export default function UploadJudgment() {
  const inputRef = useRef(null);
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function submit(selectedFile = file) {
    if (!selectedFile) return;
    setLoading(true);
    setError("");
    try {
      const result = await uploadJudgment(selectedFile);
      navigate(`/review/${result.judgment.id}`);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section>
      <WorkflowTracker current={1} />
      <div className="section-title"><h2>Upload Judgment PDF</h2><p>Extract text, metadata, directive paragraphs, and draft compliance actions.</p></div>
      <div
        className="dropzone"
        onClick={() => inputRef.current?.click()}
        onDragOver={(event) => event.preventDefault()}
        onDrop={(event) => {
          event.preventDefault();
          const dropped = event.dataTransfer.files[0];
          setFile(dropped);
          submit(dropped);
        }}
      >
        <UploadCloud size={36} />
        <h3>{file ? file.name : "Drop a court judgment PDF here"}</h3>
        <p>PDF text extraction runs first. OCR fallback is used for scanned pages.</p>
        <input ref={inputRef} hidden type="file" accept="application/pdf" onChange={(event) => setFile(event.target.files[0])} />
      </div>
      <div className="toolbar">
        <button className="button" disabled={!file || loading} onClick={() => submit()}>{loading ? "Extracting..." : "Start extraction"}</button>
        {error && <span className="inline-error">{error}</span>}
      </div>
    </section>
  );
}

