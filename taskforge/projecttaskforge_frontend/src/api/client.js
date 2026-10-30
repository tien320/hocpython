const DEFAULT_API_URL = "";
const API_URL_KEY = "taskforge-api-url";
const TOKEN_KEY = "taskforge-access-token";

export function getApiUrl() {
  const savedUrl = localStorage.getItem(API_URL_KEY) || DEFAULT_API_URL;
  if (savedUrl === "http://localhost:8000" || savedUrl === "http://127.0.0.1:8000") {
    return DEFAULT_API_URL;
  }
  return savedUrl.replace(/\/+$/, "");
}

export function saveApiUrl(value) {
  const normalized = value.trim().replace(/\/+$/, "");
  if (normalized && !/^https?:\/\//i.test(normalized)) {
    throw new Error("Địa chỉ API phải bắt đầu bằng http:// hoặc https://.");
  }
  localStorage.setItem(API_URL_KEY, normalized);
  return normalized;
}

export function getToken() {
  return sessionStorage.getItem(TOKEN_KEY);
}

export function saveToken(token) {
  sessionStorage.setItem(TOKEN_KEY, token);
}

export function clearToken() {
  sessionStorage.removeItem(TOKEN_KEY);
}

async function request(path, { method = "GET", body, formData = false } = {}) {
  const headers = new Headers();
  const token = getToken();
  if (token) headers.set("Authorization", `Bearer ${token}`);
  if (body !== undefined && !formData) headers.set("Content-Type", "application/json");

  let response;
  try {
    const apiUrl = getApiUrl();
    response = await fetch(`${apiUrl}/api/v1${path}`, {
      method,
      headers,
      body: body === undefined ? undefined : formData ? body : JSON.stringify(body),
    });
  } catch {
    const apiUrl = getApiUrl() || window.location.origin;
    throw new Error(`Không thể kết nối API tại ${apiUrl}. Hãy kiểm tra backend và địa chỉ API.`);
  }

  if (response.status === 204) return null;
  const contentType = response.headers.get("content-type") || "";
  const data = contentType.includes("application/json") ? await response.json() : await response.text();
  if (!response.ok) {
    const detail = typeof data === "object" && data !== null ? data.detail : data;
    const message = Array.isArray(detail)
      ? detail.map((item) => item.msg || JSON.stringify(item)).join(", ")
      : detail || `Yêu cầu thất bại (${response.status}).`;
    const error = new Error(String(message));
    error.status = response.status;
    throw error;
  }
  return data;
}

export const api = {
  register: (data) => request("/auth/register", { method: "POST", body: data }),
  login: (email, password) => {
    const form = new URLSearchParams({ username: email, password });
    return request("/auth/login", { method: "POST", body: form, formData: true });
  },
  me: () => request("/users/me"),
  updateProfile: (userId, data) => request(`/users/${userId}`, { method: "PUT", body: data }),

  listWorkspaces: () => request("/workspaces"),
  createWorkspace: (data) => request("/workspaces", { method: "POST", body: data }),
  getWorkspace: (id) => request(`/workspaces/${id}`),
  updateWorkspace: (id, data) => request(`/workspaces/${id}`, { method: "PUT", body: data }),
  deleteWorkspace: (id) => request(`/workspaces/${id}`, { method: "DELETE" }),
  searchWorkspaceMemberCandidates: (workspaceId, search) => {
    const query = new URLSearchParams({ q: search });
    return request(`/workspaces/${workspaceId}/member-candidates?${query.toString()}`);
  },
  listMembers: (workspaceId) => request(`/workspaces/${workspaceId}/members`),
  addMember: (workspaceId, data) => request(`/workspaces/${workspaceId}/members`, { method: "POST", body: data }),
  removeMember: (workspaceId, userId) => request(`/workspaces/${workspaceId}/members/${userId}`, { method: "DELETE" }),

  createProject: (workspaceId, data) => request(`/workspaces/${workspaceId}/projects`, { method: "POST", body: data }),
  getProject: (id) => request(`/projects/${id}`),
  updateProject: (id, data) => request(`/projects/${id}`, { method: "PATCH", body: data }),
  deleteProject: (id) => request(`/projects/${id}`, { method: "DELETE" }),

  listTasks: (projectId, filters = {}) => {
    const query = new URLSearchParams();
    Object.entries(filters).forEach(([key, value]) => {
      if (value) query.set(key, value);
    });
    const suffix = query.size ? `?${query.toString()}` : "";
    return request(`/projects/${projectId}/tasks${suffix}`);
  },
  createTask: (projectId, data) => request(`/projects/${projectId}/tasks`, { method: "POST", body: data }),
  getTask: (id) => request(`/tasks/${id}`),
  updateTask: (id, data) => request(`/tasks/${id}`, { method: "PATCH", body: data }),
  deleteTask: (id) => request(`/tasks/${id}`, { method: "DELETE" }),

  listComments: (taskId) => request(`/tasks/${taskId}/comments`),
  createComment: (taskId, data) => request(`/tasks/${taskId}/comments`, { method: "POST", body: data }),
  updateComment: (id, data) => request(`/comments/${id}`, { method: "PATCH", body: data }),
  deleteComment: (id) => request(`/comments/${id}`, { method: "DELETE" }),
};
