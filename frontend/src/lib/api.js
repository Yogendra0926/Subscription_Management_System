const API_URL = (process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000").replace(/\/$/, "");

export async function apiRequest(path, options = {}) {
  const token = typeof window === "undefined" ? null : localStorage.getItem("brightloop_token");
  const headers = new Headers(options.headers);

  if (options.body && !(options.body instanceof FormData) && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(`${API_URL}${path}`, { ...options, headers });
  const contentType = response.headers.get("content-type") || "";
  const body = contentType.includes("application/json")
    ? await response.json()
    : await response.text();

  if (!response.ok) {
    const detail = typeof body === "object" && body?.detail ? body.detail : body;
    throw new Error(detail || `Request failed with status ${response.status}`);
  }
  return body;
}

export async function login(email, password) {
  const form = new URLSearchParams({ username: email, password });
  return apiRequest("/api/auth/login", {
    method: "POST",
    body: form,
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
}

export { API_URL };
