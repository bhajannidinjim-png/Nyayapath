import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import Filters from "../components/Filters.jsx";
import StatusBadge from "../components/StatusBadge.jsx";
import { EmptyState, ErrorState, LoadingState } from "../components/StateBlock.jsx";
import { useAsync } from "../hooks/useAsync.js";
import { getActions } from "../services/api.js";

export default function ApprovedActions() {
  const [search, setSearch] = useState("");
  const [department, setDepartment] = useState("");
  const { data, loading, error } = useAsync(() => getActions({ status: "approved", department, search }), [department, search]);
  const actions = data || [];
  const departments = useMemo(() => [...new Set(actions.map((action) => action.department))], [actions]);

  if (loading) return <LoadingState label="Loading approved actions..." />;
  if (error) return <ErrorState message={error} />;

  return (
    <section>
      <div className="section-title"><h2>Approved Actions</h2><p>Verified records stored for compliance workflow tracking.</p></div>
      <Filters search={search} onSearch={setSearch} department={department} onDepartment={setDepartment} departments={departments} />
      {actions.length ? (
        <div className="table-wrap">
          <table>
            <thead><tr><th>Action</th><th>Department</th><th>Priority</th><th>Deadline</th><th></th></tr></thead>
            <tbody>
              {actions.map((action) => (
                <tr key={action.id}>
                  <td>{action.action_summary}</td>
                  <td>{action.department}</td>
                  <td><StatusBadge value={action.priority} type="priority" /></td>
                  <td>{action.deadline}</td>
                  <td><Link className="text-link" to={`/actions/${action.id}`}>Details</Link></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : <EmptyState title="No approved records" message="Approved actions will be listed in this registry." />}
    </section>
  );
}

