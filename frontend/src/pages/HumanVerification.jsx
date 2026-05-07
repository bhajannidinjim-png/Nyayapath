import { useMemo, useState } from "react";
import ActionCard from "../components/ActionCard.jsx";
import EditActionModal from "../components/EditActionModal.jsx";
import { EmptyState, ErrorState, LoadingState } from "../components/StateBlock.jsx";
import WorkflowTracker from "../components/WorkflowTracker.jsx";
import { useAsync } from "../hooks/useAsync.js";
import { getActions, verifyAction } from "../services/api.js";

export default function HumanVerification() {
  const [editing, setEditing] = useState(null);
  const { data, loading, error, reload } = useAsync(() => getActions({ status: "pending" }), []);
  const pending = useMemo(() => data || [], [data]);

  async function update(action, status, edits = {}) {
    await verifyAction(action.id, { ...edits, status });
    setEditing(null);
    reload();
  }

  if (loading) return <LoadingState label="Loading pending actions..." />;
  if (error) return <ErrorState message={error} />;

  return (
    <section>
      <WorkflowTracker current={4} />
      <div className="section-title"><h2>Human Verification</h2><p>Approve, edit, or reject AI-assisted extraction outputs before publication.</p></div>
      {pending.length ? pending.map((action) => (
        <ActionCard key={action.id} action={action}>
          <button className="button secondary" onClick={() => setEditing(action)}>Edit</button>
          <button className="button reject" onClick={() => update(action, "rejected")}>Reject</button>
          <button className="button approve" onClick={() => update(action, "approved")}>Approve</button>
        </ActionCard>
      )) : <EmptyState title="No pending actions" message="Upload a judgment or review previously extracted records." />}
      {editing && <EditActionModal action={editing} onClose={() => setEditing(null)} onSubmit={(form) => update(editing, "approved", form)} />}
    </section>
  );
}

