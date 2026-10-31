export default function StatusBadge({ status }) {
  return <span className={`badge ${String(status).toLowerCase().replace(" ", "-")}`}>{status}</span>;
}
