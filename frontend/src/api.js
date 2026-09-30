const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function request(path, options = {}) {
  const token = localStorage.getItem("agentguard_token");
  const headers = { ...(options.headers || {}) };
  if (token) headers.Authorization = `Bearer ${token}`;
  const response = await fetch(`${API_URL}${path}`, { ...options, headers });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.detail || "Request failed");
  return data;
}

export function login(email, password) {
  return request("/api/auth/login", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({email, password}),
  });
}

export function evaluateAction(payload) {
  return request("/api/actions/evaluate", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(payload),
  });
}

export async function uploadFile(file, classification) {
  const form = new FormData();
  form.append("file", file);
  form.append("classification", classification);
  return request("/api/files/upload", {method: "POST", body: form});
}

export function getFiles() { return request("/api/files"); }
export function getApprovals() { return request("/api/approvals"); }
export function getAudit() { return request("/api/audit"); }
export function getStats() { return request("/api/audit/stats"); }

export function resolveApproval(id, approved, reason) {
  return request(`/api/approvals/${id}`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({approved, reason}),
  });
}
