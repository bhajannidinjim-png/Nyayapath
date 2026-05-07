export function LoadingState({ label = "Loading records..." }) {
  return <div className="state-block"><div className="spinner" /> <span>{label}</span></div>;
}

export function ErrorState({ message }) {
  return <div className="state-block error-state">{message}</div>;
}

export function EmptyState({ title, message }) {
  return <div className="empty-state"><h3>{title}</h3><p>{message}</p></div>;
}

