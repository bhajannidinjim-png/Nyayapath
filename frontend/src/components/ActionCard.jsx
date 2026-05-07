import { Link } from "react-router-dom";
import ConfidenceBadge from "./ConfidenceBadge.jsx";
import EvidenceAccordion from "./EvidenceAccordion.jsx";
import StatusBadge from "./StatusBadge.jsx";

export default function ActionCard({ action, compact = false, children }) {
  return (
    <article className="action-card">
      <div className="card-head">
        <div>
          <StatusBadge value={action.action_type} type="action" />
          <h3>{action.action_summary}</h3>
        </div>
        <ConfidenceBadge value={action.confidence} />
      </div>
      <div className="meta-grid">
        <span><strong>Department</strong>{action.department}</span>
        <span><strong>Priority</strong><StatusBadge value={action.priority} type="priority" /></span>
        <span><strong>Deadline</strong>{action.deadline}</span>
        <span><strong>Status</strong><StatusBadge value={action.verification_status} type="verify" /></span>
      </div>
      {!compact && <EvidenceAccordion sourceText={action.source_text} reason={action.extraction_reason} pageReference={action.page_reference} />}
      <div className="card-actions">
        <Link className="text-link" to={`/actions/${action.id}`}>Open details</Link>
        {children}
      </div>
    </article>
  );
}

