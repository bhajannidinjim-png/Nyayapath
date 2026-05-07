export default function Filters({ search, onSearch, department, onDepartment, departments = [] }) {
  return (
    <div className="filters">
      <input value={search} onChange={(event) => onSearch(event.target.value)} placeholder="Search actions or evidence" />
      <select value={department} onChange={(event) => onDepartment(event.target.value)}>
        <option value="">All departments</option>
        {departments.map((item) => <option key={item} value={item}>{item}</option>)}
      </select>
    </div>
  );
}

