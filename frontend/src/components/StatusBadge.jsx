export default function StatusBadge({ value, type = "status" }) {
  const normalized = String(value || "").toLowerCase().replaceAll(" ", "-");
  return <span className={`badge ${type}-${normalized}`}>{value}</span>;
}

