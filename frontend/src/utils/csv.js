const escape = (value) => `"${String(value ?? "").replaceAll('"', '""')}"`;

export function downloadCsv(filename, rows) {
  if (!rows.length || typeof window === "undefined") return false;
  const headers = [...new Set(rows.flatMap((row) => Object.keys(row)))];
  const csv = [headers.join(","), ...rows.map((row) => headers.map((header) => escape(row[header])).join(","))].join("\n");
  const url = URL.createObjectURL(new Blob([csv], { type: "text/csv;charset=utf-8" }));
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
  return true;
}
