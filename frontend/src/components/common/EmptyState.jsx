import { Inbox } from "lucide-react";
export default function EmptyState({ title = "No records found", description = "Try changing your filters or create a new record." }) {
  return <div className="empty-state"><Inbox size={28}/><b>{title}</b><span>{description}</span></div>;
}
