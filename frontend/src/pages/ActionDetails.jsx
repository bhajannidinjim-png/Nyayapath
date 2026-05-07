import { useParams } from "react-router-dom";
import ActionCard from "../components/ActionCard.jsx";
import { ErrorState, LoadingState } from "../components/StateBlock.jsx";
import { useAsync } from "../hooks/useAsync.js";
import { getAction } from "../services/api.js";

export default function ActionDetails() {
  const { actionId } = useParams();
  const { data, loading, error } = useAsync(() => getAction(actionId), [actionId]);
  if (loading) return <LoadingState label="Loading action details..." />;
  if (error) return <ErrorState message={error} />;

  return (
    <section>
      <div className="section-title"><h2>Action Details</h2><p>Explainable extraction record with reviewer status.</p></div>
      <ActionCard action={data} />
      <div className="panel">
        <h3>Decision Support Notes</h3>
        <p><strong>Compliance requirement:</strong> {data.compliance_requirement}</p>
        <p><strong>Appeal consideration:</strong> {data.appeal_consideration}</p>
        <p><strong>Reviewer notes:</strong> {data.reviewer_notes || "No reviewer notes recorded."}</p>
      </div>
    </section>
  );
}

