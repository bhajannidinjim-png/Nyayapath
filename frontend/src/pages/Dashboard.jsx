import { useMemo, useState } from "react";
import ActionCard from "../components/ActionCard.jsx";
import Filters from "../components/Filters.jsx";
import { EmptyState, ErrorState, LoadingState } from "../components/StateBlock.jsx";
import { useAsync } from "../hooks/useAsync.js";
import { getActions } from "../services/api.js";

export default function Dashboard() {
  const [search, setSearch] = useState("");
  const [department, setDepartment] = useState("");
  const { data, loading, error } = useAsync(() => getActions({ status: "approved", department, search }), [department, search]);
  const actions = data || [];
  const departments = useMemo(() => [...new Set(actions.map((action) => action.department))], [actions]);
  const high = actions.filter((action) => action.priority === "High").length;

  if (loading) return <LoadingState label="Loading approved dashboard..." />;
  if (error) return <ErrorState message={error} />;

  return (
    <section>
      <div className="section-title"><h2>Dashboard</h2><p>Approved compliance actions ready for departmental tracking.</p></div>
      <div className="stats-row">
        <div><strong>{actions.length}</strong><span>Approved actions</span></div>
        <div><strong>{departments.length}</strong><span>Departments</span></div>
        <div><strong>{high}</strong><span>High priority</span></div>
      </div>
      <Filters search={search} onSearch={setSearch} department={department} onDepartment={setDepartment} departments={departments} />
      {actions.length ? actions.map((action) => <ActionCard key={action.id} action={action} compact />) : <EmptyState title="No approved actions yet" message="Actions appear here only after a reviewer approves them." />}
    </section>
  );
}

