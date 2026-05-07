import { useState } from "react";

export default function EditActionModal({ action, onClose, onSubmit }) {
  const [form, setForm] = useState({
    action_type: action.action_type,
    action_summary: action.action_summary,
    department: action.department,
    deadline: action.deadline,
    priority: action.priority,
    compliance_requirement: action.compliance_requirement,
    appeal_consideration: action.appeal_consideration,
    reviewer_notes: action.reviewer_notes || ""
  });

  function update(field, value) {
    setForm((current) => ({ ...current, [field]: value }));
  }

  return (
    <div className="modal-backdrop">
      <form className="modal" onSubmit={(event) => { event.preventDefault(); onSubmit(form); }}>
        <h2>Edit action before approval</h2>
        <label>Summary<textarea value={form.action_summary} onChange={(event) => update("action_summary", event.target.value)} /></label>
        <div className="two-col">
          <label>Type<input value={form.action_type} onChange={(event) => update("action_type", event.target.value)} /></label>
          <label>Department<input value={form.department} onChange={(event) => update("department", event.target.value)} /></label>
        </div>
        <div className="two-col">
          <label>Deadline<input value={form.deadline} onChange={(event) => update("deadline", event.target.value)} /></label>
          <label>Priority<select value={form.priority} onChange={(event) => update("priority", event.target.value)}><option>High</option><option>Medium</option><option>Low</option></select></label>
        </div>
        <label>Reviewer notes<textarea value={form.reviewer_notes} onChange={(event) => update("reviewer_notes", event.target.value)} /></label>
        <div className="modal-actions">
          <button type="button" className="button secondary" onClick={onClose}>Cancel</button>
          <button className="button">Save changes</button>
        </div>
      </form>
    </div>
  );
}

