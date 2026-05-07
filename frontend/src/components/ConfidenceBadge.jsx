export default function ConfidenceBadge({ value }) {
  const score = Number(value || 0);
  const label = score >= 0.75 ? "High" : score >= 0.5 ? "Medium" : "Low";
  return <span className={`confidence confidence-${label.toLowerCase()}`}>{label} {Math.round(score * 100)}%</span>;
}

