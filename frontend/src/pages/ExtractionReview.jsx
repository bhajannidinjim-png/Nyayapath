import { Link, useParams } from "react-router-dom";
import ActionCard from "../components/ActionCard.jsx";
import { EmptyState, ErrorState, LoadingState } from "../components/StateBlock.jsx";
import WorkflowTracker from "../components/WorkflowTracker.jsx";
import { useAsync } from "../hooks/useAsync.js";
import { getJudgment } from "../services/api.js";

export default function ExtractionReview() {
  const { judgmentId } = useParams();
  const { data, loading, error } = useAsync(() => getJudgment(judgmentId), [judgmentId]);
  if (loading) return <LoadingState label="Reviewing extracted judgment..." />;
  if (error) return <ErrorState message={error} />;

  const metadata = data.metadata_json || {};
  return (
    <section>
      <WorkflowTracker current={3} />
      <div className="section-title"><h2>Extraction Review</h2><p>{data.filename}</p></div>
      <div className="stats-row">
        <div><strong>{data.total_pages}</strong><span>Pages</span></div>
        <div><strong>{data.scanned_pages.length}</strong><span>Scanned pages</span></div>
        <div><strong>{data.actions.length}</strong><span>Draft actions</span></div>
      </div>
      <div className="panel">
        <h3>Structured Metadata</h3>
        <div className="metadata-grid">
          {Object.entries(metadata).map(([key, field]) => (
            <div key={key}>
              <strong>{key.replaceAll("_", " ")}</strong>
              <span>{field.value}</span>
              <small>{Math.round((field.confidence || 0) * 100)}% confidence</small>
            </div>
          ))}
        </div>
      </div>
      <div className="section-title compact"><h2>Detected Directive Actions</h2><Link className="button" to="/verify">Proceed to verification</Link></div>
      {data.actions.length ? data.actions.map((action) => <ActionCard key={action.id} action={action} />) : <EmptyState title="No actions detected" message="The reviewer can still inspect extracted page text from the stored judgment record." />}
    </section>
  );
}

