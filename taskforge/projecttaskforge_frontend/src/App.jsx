import React, { useEffect, useMemo, useState } from "react";
import { api, getApiUrl, saveApiUrl } from "./api/client.js";
import { useAuth } from "./context/AuthContext.jsx";

const STATUSES = ["TODO", "IN_PROGRESS", "IN_REVIEW", "DONE", "CANCELLED"];
const PRIORITIES = ["LOW", "MEDIUM", "HIGH", "CRITICAL"];
const STATUS_LABELS = {
  TODO: "Cần làm",
  IN_PROGRESS: "Đang làm",
  IN_REVIEW: "Đang duyệt",
  DONE: "Hoàn thành",
  CANCELLED: "Đã hủy",
};
const PRIORITY_LABELS = { LOW: "Thấp", MEDIUM: "Trung bình", HIGH: "Cao", CRITICAL: "Khẩn cấp" };
const WORKSPACES_KEY = "taskforge-workspaces";
const PROJECTS_KEY = "taskforge-projects";

function readStored(key) {
  try {
    return JSON.parse(localStorage.getItem(key) || "[]");
  } catch {
    return [];
  }
}

function saveStored(key, value) {
  localStorage.setItem(key, JSON.stringify(value));
}

function getWorkspaceIds() {
  return readStored(WORKSPACES_KEY);
}

function getProjectEntries(workspaceId) {
  return readStored(PROJECTS_KEY).filter((project) => project.workspaceId === workspaceId);
}

function rememberWorkspace(workspace) {
  const workspaces = getWorkspaceIds().filter((item) => item.id !== workspace.id);
  saveStored(WORKSPACES_KEY, [{ id: workspace.id, name: workspace.name }, ...workspaces]);
}

function rememberProject(project) {
  const projects = readStored(PROJECTS_KEY).filter((item) => item.id !== project.id);
  saveStored(PROJECTS_KEY, [
    { id: project.id, workspaceId: project.workspace_id, name: project.name, key: project.key },
    ...projects,
  ]);
}

function initials(name = "") {
  return name.trim().split(/\s+/).slice(0, 2).map((part) => part[0]).join("").toUpperCase() || "TF";
}

function dateLabel(value) {
  if (!value) return "";
  return new Intl.DateTimeFormat("vi-VN", { day: "2-digit", month: "short" }).format(new Date(value));
}

function ErrorMessage({ children }) {
  return children ? <div className="notice error" role="alert">{children}</div> : null;
}

function Modal({ title, onClose, children, wide = false }) {
  useEffect(() => {
    const onKeyDown = (event) => event.key === "Escape" && onClose();
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [onClose]);
  return (
    <div className="modal-backdrop" onMouseDown={(event) => event.target === event.currentTarget && onClose()}>
      <section className={`modal${wide ? " modal-wide" : ""}`} role="dialog" aria-modal="true" aria-label={title}>
        <div className="modal-heading">
          <h2>{title}</h2>
          <button className="icon-button" type="button" onClick={onClose} aria-label="Đóng">×</button>
        </div>
        {children}
      </section>
    </div>
  );
}

function AuthScreen() {
  const { login, register, authError } = useAuth();
  const [mode, setMode] = useState("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [apiUrl, setApiUrl] = useState(getApiUrl());
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit(event) {
    event.preventDefault();
    setBusy(true);
    setError("");
    try {
      saveApiUrl(apiUrl);
      if (mode === "register") {
        await register({ email, password, full_name: fullName });
      } else {
        await login(email, password);
      }
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="auth-page">
      <div className="auth-art">
        <div className="brand brand-light"><span className="brand-mark">T</span> TaskForge</div>
        <div className="art-copy">
          <p className="eyebrow">LÀM VIỆC NHÓM, DỄ DÀNG HƠN</p>
          <h1>Mọi dự án.<br />Một nhịp tiến.</h1>
          <p>Tổ chức công việc, theo dõi tiến độ và cùng nhau hoàn thành những điều quan trọng.</p>
          <div className="art-shapes"><span /><span /><span /></div>
        </div>
        <p className="art-foot">Không gian làm việc của bạn, được sắp xếp gọn gàng.</p>
      </div>
      <div className="auth-panel">
        <div className="auth-card">
          <div className="brand mobile-brand"><span className="brand-mark">T</span> TaskForge</div>
          <p className="eyebrow">BẮT ĐẦU NGAY</p>
          <h2>{mode === "login" ? "Chào mừng trở lại" : "Tạo tài khoản mới"}</h2>
          <p className="muted">{mode === "login" ? "Đăng nhập để tiếp tục công việc của bạn." : "Tạo tài khoản để bắt đầu quản lý dự án."}</p>
          <form className="stack-form" onSubmit={submit}>
            {mode === "register" && (
              <label>Họ và tên
                <input autoComplete="name" value={fullName} onChange={(event) => setFullName(event.target.value)} required maxLength={255} />
              </label>
            )}
            <label>Email
              <input type="email" autoComplete="email" value={email} onChange={(event) => setEmail(event.target.value)} required />
            </label>
            <label>Mật khẩu
              <input type="password" autoComplete={mode === "login" ? "current-password" : "new-password"} value={password} onChange={(event) => setPassword(event.target.value)} required minLength={6} />
            </label>
            <label>Địa chỉ backend API
              <input value={apiUrl} onChange={(event) => setApiUrl(event.target.value)} placeholder="Để trống để dùng cùng origin" />
              <span className="field-hint">Để trống để dùng cùng origin; Vite chuyển tiếp /api/v1 đến backend cục bộ.</span>
            </label>
            <ErrorMessage>{error || authError}</ErrorMessage>
            <button className="button primary full" disabled={busy}>{busy ? "Đang xử lý..." : mode === "login" ? "Đăng nhập" : "Tạo tài khoản"}</button>
          </form>
          <p className="auth-switch">
            {mode === "login" ? "Chưa có tài khoản?" : "Đã có tài khoản?"}{" "}
            <button type="button" className="text-button" onClick={() => { setMode(mode === "login" ? "register" : "login"); setError(""); }}>
              {mode === "login" ? "Đăng ký" : "Đăng nhập"}
            </button>
          </p>
        </div>
      </div>
    </main>
  );
}

function WorkspaceDialog({ onClose, onCreated }) {
  const [name, setName] = useState("");
  const [slug, setSlug] = useState("");
  const [workspaceId, setWorkspaceId] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [view, setView] = useState("create");

  async function create(event) {
    event.preventDefault();
    setBusy(true);
    setError("");
    try {
      const workspace = await api.createWorkspace({ name, slug });
      rememberWorkspace(workspace);
      onCreated(workspace);
      onClose();
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setBusy(false);
    }
  }

  async function openExisting(event) {
    event.preventDefault();
    setBusy(true);
    setError("");
    try {
      const workspace = await api.getWorkspace(workspaceId.trim());
      rememberWorkspace(workspace);
      onCreated(workspace);
      onClose();
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <Modal title="Không gian làm việc" onClose={onClose}>
      <div className="segmented">
        <button className={view === "create" ? "selected" : ""} onClick={() => setView("create")}>Tạo mới</button>
        <button className={view === "open" ? "selected" : ""} onClick={() => setView("open")}>Mở bằng ID</button>
      </div>
      {view === "create" ? (
        <form className="stack-form" onSubmit={create}>
          <label>Tên workspace<input value={name} onChange={(event) => setName(event.target.value)} required maxLength={255} placeholder="Ví dụ: Đội sản phẩm" /></label>
          <label>Đường dẫn (slug)<input value={slug} onChange={(event) => setSlug(event.target.value.toLowerCase().replace(/[^a-z0-9-]/g, "-"))} pattern="[a-z0-9-]+" required maxLength={255} placeholder="doi-san-pham" /></label>
          <p className="field-hint">Bạn sẽ trở thành chủ sở hữu workspace mới.</p>
          <ErrorMessage>{error}</ErrorMessage>
          <button className="button primary" disabled={busy}>{busy ? "Đang tạo..." : "Tạo workspace"}</button>
        </form>
      ) : (
        <form className="stack-form" onSubmit={openExisting}>
          <label>Workspace ID<input value={workspaceId} onChange={(event) => setWorkspaceId(event.target.value)} required placeholder="UUID của workspace" /></label>
          <p className="field-hint">Backend hiện chưa có API liệt kê workspace; dùng ID bạn đã nhận được.</p>
          <ErrorMessage>{error}</ErrorMessage>
          <button className="button primary" disabled={busy}>{busy ? "Đang tải..." : "Mở workspace"}</button>
        </form>
      )}
    </Modal>
  );
}

function ProjectDialog({ workspace, onClose, onCreated }) {
  const [name, setName] = useState("");
  const [key, setKey] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit(event) {
    event.preventDefault();
    setBusy(true);
    setError("");
    try {
      const project = await api.createProject(workspace.id, { name, key: key.toUpperCase(), description: description || null });
      rememberProject(project);
      onCreated(project);
      onClose();
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <Modal title="Tạo dự án" onClose={onClose}>
      <form className="stack-form" onSubmit={submit}>
        <label>Tên dự án<input value={name} onChange={(event) => setName(event.target.value)} required maxLength={255} placeholder="Ví dụ: Website mới" /></label>
        <label>Mã dự án<input value={key} onChange={(event) => setKey(event.target.value.toUpperCase().replace(/[^A-Z0-9_]/g, ""))} required maxLength={32} pattern="[A-Z0-9_]+" placeholder="WEB" /></label>
        <label>Mô tả<textarea value={description} onChange={(event) => setDescription(event.target.value)} rows={3} /></label>
        <ErrorMessage>{error}</ErrorMessage>
        <button className="button primary" disabled={busy}>{busy ? "Đang tạo..." : "Tạo dự án"}</button>
      </form>
    </Modal>
  );
}

function EditProjectDialog({ project, onClose, onSaved }) {
  const [name, setName] = useState(project.name);
  const [description, setDescription] = useState(project.description || "");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit(event) {
    event.preventDefault();
    setBusy(true);
    setError("");
    try {
      const updated = await api.updateProject(project.id, { name, description: description || null });
      rememberProject(updated);
      onSaved(updated);
      onClose();
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <Modal title="Cập nhật dự án" onClose={onClose}>
      <form className="stack-form" onSubmit={submit}>
        <label>Tên dự án<input value={name} onChange={(event) => setName(event.target.value)} required maxLength={255} /></label>
        <label>Mã dự án<input value={project.key} disabled /><span className="field-hint">Backend hiện không cho phép đổi mã dự án.</span></label>
        <label>Mô tả<textarea value={description} onChange={(event) => setDescription(event.target.value)} rows={4} /></label>
        <ErrorMessage>{error}</ErrorMessage>
        <div className="dialog-actions">
          <span className="spacer" />
          <button type="button" className="button secondary" onClick={onClose}>Hủy</button>
          <button className="button primary" disabled={busy}>{busy ? "Đang lưu..." : "Lưu thay đổi"}</button>
        </div>
      </form>
    </Modal>
  );
}

function TaskDialog({ project, task, members, onClose, onSaved, onDeleted }) {
  const [title, setTitle] = useState(task?.title || "");
  const [description, setDescription] = useState(task?.description || "");
  const [status, setStatus] = useState(task?.status || "TODO");
  const [priority, setPriority] = useState(task?.priority || "MEDIUM");
  const [assigneeId, setAssigneeId] = useState(task?.assignee_id || "");
  const [comments, setComments] = useState([]);
  const [commentText, setCommentText] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [commentsLoading, setCommentsLoading] = useState(Boolean(task));
  const isEditing = Boolean(task);

  useEffect(() => {
    if (!task) return;
    api.listComments(task.id)
      .then(setComments)
      .catch((requestError) => setError(requestError.message))
      .finally(() => setCommentsLoading(false));
  }, [task]);

  async function submit(event) {
    event.preventDefault();
    setBusy(true);
    setError("");
    try {
      const payload = {
        title,
        description: description || null,
        priority,
        ...(isEditing ? { status, assignee_id: assigneeId || null } : { assignee_id: assigneeId || null }),
      };
      const saved = isEditing
        ? await api.updateTask(task.id, payload)
        : await api.createTask(project.id, payload);
      await onSaved(saved);
      onClose();
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setBusy(false);
    }
  }

  async function addComment(event) {
    event.preventDefault();
    if (!commentText.trim()) return;
    setBusy(true);
    setError("");
    try {
      const created = await api.createComment(task.id, { content: commentText.trim() });
      setComments((current) => [...current, created]);
      setCommentText("");
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setBusy(false);
    }
  }

  async function editComment(comment) {
    const content = window.prompt("Chỉnh sửa bình luận", comment.content);
    if (content === null || !content.trim()) return;
    setError("");
    try {
      const updated = await api.updateComment(comment.id, { content: content.trim() });
      setComments((current) => current.map((item) => item.id === updated.id ? updated : item));
    } catch (requestError) {
      setError(requestError.message);
    }
  }

  async function removeComment(comment) {
    if (!window.confirm("Bạn có chắc muốn xóa bình luận này?")) return;
    setError("");
    try {
      await api.deleteComment(comment.id);
      setComments((current) => current.filter((item) => item.id !== comment.id));
    } catch (requestError) {
      setError(requestError.message);
    }
  }

  async function removeTask() {
    if (!window.confirm("Xóa công việc này? Thao tác không thể hoàn tác.")) return;
    setBusy(true);
    setError("");
    try {
      await api.deleteTask(task.id);
      onDeleted(task.id);
      onClose();
    } catch (requestError) {
      setError(requestError.message);
      setBusy(false);
    }
  }

  return (
    <Modal title={isEditing ? "Chi tiết công việc" : "Tạo công việc"} onClose={onClose} wide>
      <form className="stack-form" onSubmit={submit}>
        <label>Tiêu đề<input value={title} onChange={(event) => setTitle(event.target.value)} required maxLength={255} placeholder="Bạn cần hoàn thành việc gì?" /></label>
        <label>Mô tả<textarea value={description} onChange={(event) => setDescription(event.target.value)} rows={3} placeholder="Thêm thông tin cho công việc..." /></label>
        <div className="form-grid">
          <label>Độ ưu tiên
            <select value={priority} onChange={(event) => setPriority(event.target.value)}>
              {PRIORITIES.map((value) => <option key={value} value={value}>{PRIORITY_LABELS[value]}</option>)}
            </select>
          </label>
          {isEditing && <label>Trạng thái
            <select value={status} onChange={(event) => setStatus(event.target.value)}>
              {STATUSES.map((value) => <option key={value} value={value}>{STATUS_LABELS[value]}</option>)}
            </select>
          </label>}
          <label className={isEditing ? "" : "form-span"}>Người thực hiện
            <select value={assigneeId} onChange={(event) => setAssigneeId(event.target.value)}>
              <option value="">Chưa giao</option>
              {members.map((member) => <option key={member.user_id} value={member.user_id}>{member.user?.full_name || member.user?.email || member.user_id}</option>)}
            </select>
          </label>
        </div>
        <ErrorMessage>{error}</ErrorMessage>
        <div className="dialog-actions">
          {isEditing && <button type="button" className="button danger-quiet" onClick={removeTask} disabled={busy}>Xóa công việc</button>}
          <span className="spacer" />
          <button type="button" className="button secondary" onClick={onClose}>Đóng</button>
          <button className="button primary" disabled={busy}>{busy ? "Đang lưu..." : isEditing ? "Lưu thay đổi" : "Tạo công việc"}</button>
        </div>
      </form>
      {isEditing && (
        <section className="comments-section">
          <div className="section-line"><h3>Bình luận</h3><span>{comments.length}</span></div>
          {commentsLoading ? <p className="muted">Đang tải bình luận...</p> : comments.length === 0 ? <p className="empty-inline">Chưa có bình luận. Hãy bắt đầu cuộc trò chuyện.</p> : (
            <div className="comment-list">
              {comments.map((comment) => (
                <article className="comment" key={comment.id}>
                  <div className="avatar small">{initials(comment.author?.full_name || comment.author?.email)}</div>
                  <div className="comment-body">
                    <div className="comment-meta"><strong>{comment.author?.full_name || comment.author?.email || "Thành viên"}</strong><time>{dateLabel(comment.created_at)}</time></div>
                    <p>{comment.content}</p>
                    <div className="comment-actions">
                      <button type="button" onClick={() => editComment(comment)}>Sửa</button>
                      <button type="button" onClick={() => removeComment(comment)}>Xóa</button>
                    </div>
                  </div>
                </article>
              ))}
            </div>
          )}
          <form className="comment-compose" onSubmit={addComment}>
            <textarea value={commentText} onChange={(event) => setCommentText(event.target.value)} rows={2} placeholder="Viết bình luận..." />
            <button className="button primary" disabled={busy || !commentText.trim()}>Gửi</button>
          </form>
        </section>
      )}
    </Modal>
  );
}

function MembersView({ workspace, onError }) {
  const [members, setMembers] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [candidates, setCandidates] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [searchLoading, setSearchLoading] = useState(false);
  const [searchError, setSearchError] = useState("");
  const [role, setRole] = useState("MEMBER");
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);

  async function loadMembers() {
    setLoading(true);
    try {
      setMembers(await api.listMembers(workspace.id));
    } catch (error) {
      onError(error.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { loadMembers(); }, [workspace.id]);

  useEffect(() => {
    setSearchTerm("");
    setSelectedUser(null);
  }, [workspace.id]);

  const normalizedSearch = searchTerm.trim();
  useEffect(() => {
    setCandidates([]);
    setSearchError("");
    setSearchLoading(false);
    if (normalizedSearch.length < 2) return undefined;

    let active = true;
    setSearchLoading(true);
    const timeoutId = window.setTimeout(async () => {
      try {
        const results = await api.searchWorkspaceMemberCandidates(workspace.id, normalizedSearch);
        if (active) setCandidates(results);
      } catch (error) {
        if (active) setSearchError(error.message);
      } finally {
        if (active) setSearchLoading(false);
      }
    }, 300);

    return () => {
      active = false;
      window.clearTimeout(timeoutId);
    };
  }, [workspace.id, normalizedSearch]);

  async function add(event) {
    event.preventDefault();
    if (!selectedUser) return;
    setBusy(true);
    onError("");
    try {
      await api.addMember(workspace.id, { user_id: selectedUser.id, role });
      setSearchTerm("");
      setCandidates([]);
      setSelectedUser(null);
      await loadMembers();
    } catch (error) {
      onError(error.message);
    } finally {
      setBusy(false);
    }
  }

  async function remove(member) {
    if (!window.confirm(`Xóa ${member.user?.full_name || member.user?.email || "thành viên"} khỏi workspace?`)) return;
    onError("");
    try {
      await api.removeMember(workspace.id, member.user_id);
      setMembers((current) => current.filter((item) => item.user_id !== member.user_id));
    } catch (error) {
      onError(error.message);
    }
  }

  return (
    <section className="page-content">
      <div className="page-heading"><div><p className="eyebrow">KHÔNG GIAN LÀM VIỆC</p><h1>Thành viên</h1><p className="muted">Quản lý người tham gia trong {workspace.name}.</p></div></div>
      <form className="invite-card" onSubmit={add}>
        <div className="invite-copy"><strong>Thêm thành viên</strong><span>Tìm tài khoản theo tên hoặc email.</span></div>
        <div className="invite-search">
          <input
            type="search"
            value={searchTerm}
            onChange={(event) => {
              setSearchTerm(event.target.value);
              setSelectedUser(null);
            }}
            required
            minLength={2}
            maxLength={100}
            autoComplete="off"
            aria-label="Tìm user theo tên hoặc email"
            aria-describedby="member-search-status"
            placeholder="Tên hoặc email (ít nhất 2 ký tự)"
          />
          {candidates.length > 0 && !selectedUser && (
            <ul className="member-suggestions" role="listbox" aria-label="Tài khoản phù hợp">
              {candidates.map((candidate) => (
                <li key={candidate.id}>
                  <button
                    type="button"
                    role="option"
                    aria-selected="false"
                    onClick={() => {
                      setSelectedUser(candidate);
                      setCandidates([]);
                      setSearchError("");
                    }}
                  >
                    <strong>{candidate.full_name}</strong>
                    <span>{candidate.email}</span>
                  </button>
                </li>
              ))}
            </ul>
          )}
          <div className="member-search-status" id="member-search-status" aria-live="polite">
            {selectedUser && <span className="member-selection">Đã chọn: {selectedUser.full_name} ({selectedUser.email})</span>}
            {!selectedUser && searchLoading && <span className="field-hint">Đang tìm tài khoản...</span>}
            {!selectedUser && !searchLoading && normalizedSearch.length >= 2 && !searchError && candidates.length === 0 && (
              <span className="field-hint">Không tìm thấy tài khoản phù hợp.</span>
            )}
            <ErrorMessage>{searchError}</ErrorMessage>
          </div>
        </div>
        <select value={role} onChange={(event) => setRole(event.target.value)}><option value="MEMBER">Thành viên</option><option value="ADMIN">Quản trị viên</option></select>
        <button className="button primary" disabled={busy || !selectedUser}>{busy ? "Đang thêm..." : "Thêm"}</button>
      </form>
      {loading ? <div className="loading-state">Đang tải thành viên...</div> : (
        <div className="member-list">
          {members.map((member) => (
            <div className="member-row" key={member.user_id}>
              <div className="avatar">{initials(member.user?.full_name || member.user?.email)}</div>
              <div className="member-info"><strong>{member.user?.full_name || "Tài khoản TaskForge"}</strong><span>{member.user?.email || member.user_id}</span></div>
              <span className={`role-badge role-${member.role?.toLowerCase()}`}>{member.role}</span>
              <button className="button secondary small-button" onClick={() => remove(member)}>Gỡ</button>
            </div>
          ))}
          {members.length === 0 && <div className="empty-state">Chưa có thành viên nào.</div>}
        </div>
      )}
      <p className="field-hint">API hiện hỗ trợ thêm và xóa thành viên; chưa có endpoint đổi role.</p>
    </section>
  );
}

function SettingsView({ workspace, user, onWorkspaceUpdated, onWorkspaceDeleted, onProfileUpdated, onError }) {
  const [name, setName] = useState(workspace.name);
  const [slug, setSlug] = useState(workspace.slug);
  const [fullName, setFullName] = useState(user.full_name);
  const [password, setPassword] = useState("");
  const [busy, setBusy] = useState(false);

  async function updateWorkspace(event) {
    event.preventDefault();
    setBusy(true);
    onError("");
    try {
      const updated = await api.updateWorkspace(workspace.id, { name, slug });
      rememberWorkspace(updated);
      onWorkspaceUpdated(updated);
    } catch (error) {
      onError(error.message);
    } finally {
      setBusy(false);
    }
  }

  async function updateProfile(event) {
    event.preventDefault();
    setBusy(true);
    onError("");
    try {
      const data = { full_name: fullName };
      if (password) data.password = password;
      const updated = await api.updateProfile(user.id, data);
      onProfileUpdated(updated);
      setPassword("");
    } catch (error) {
      onError(error.message);
    } finally {
      setBusy(false);
    }
  }

  async function deleteWorkspace() {
    if (!window.confirm("Xóa workspace này và toàn bộ dữ liệu liên quan? Thao tác không thể hoàn tác.")) return;
    setBusy(true);
    onError("");
    try {
      await api.deleteWorkspace(workspace.id);
      onWorkspaceDeleted(workspace.id);
    } catch (error) {
      onError(error.message);
      setBusy(false);
    }
  }

  return (
    <section className="page-content">
      <div className="page-heading"><div><p className="eyebrow">TÙY CHỈNH</p><h1>Cài đặt</h1><p className="muted">Thông tin cá nhân và workspace hiện tại.</p></div></div>
      <div className="settings-grid">
        <form className="settings-card stack-form" onSubmit={updateWorkspace}>
          <div><h2>Workspace</h2><p className="muted">Cập nhật tên và đường dẫn workspace.</p></div>
          <label>Tên workspace<input value={name} onChange={(event) => setName(event.target.value)} required maxLength={255} /></label>
          <label>Slug<input value={slug} onChange={(event) => setSlug(event.target.value.toLowerCase().replace(/[^a-z0-9-]/g, "-"))} required pattern="[a-z0-9-]+" maxLength={255} /></label>
          <button className="button primary" disabled={busy}>Lưu workspace</button>
          <div className="danger-zone"><strong>Vùng nguy hiểm</strong><p>Chỉ chủ sở hữu workspace mới có quyền xóa.</p><button type="button" className="button danger-quiet" onClick={deleteWorkspace} disabled={busy}>Xóa workspace</button></div>
        </form>
        <form className="settings-card stack-form" onSubmit={updateProfile}>
          <div><h2>Tài khoản</h2><p className="muted">{user.email}</p></div>
          <label>Họ và tên<input value={fullName} onChange={(event) => setFullName(event.target.value)} required maxLength={255} /></label>
          <label>Mật khẩu mới <span className="optional">(để trống nếu không đổi)</span><input type="password" value={password} onChange={(event) => setPassword(event.target.value)} minLength={6} /></label>
          <button className="button primary" disabled={busy}>Lưu tài khoản</button>
          <p className="field-hint">Cập nhật email chưa được backend hỗ trợ.</p>
        </form>
      </div>
    </section>
  );
}

function TaskCard({ task, onClick }) {
  return (
    <button className="task-card" onClick={onClick}>
      <div className="task-card-top"><span className={`priority-dot priority-${task.priority?.toLowerCase()}`} /> <span>{task.priority ? PRIORITY_LABELS[task.priority] : ""}</span><span className="task-date">{dateLabel(task.updated_at)}</span></div>
      <strong>{task.title}</strong>
      {task.description && <p>{task.description}</p>}
      <div className="task-card-bottom">
        <span className="task-key">{task.id?.slice(0, 8).toUpperCase()}</span>
        <span className="task-assignee">{task.assignee ? initials(task.assignee.full_name) : "—"}</span>
      </div>
    </button>
  );
}

function App() {
  const { user, loading, logout, setUser } = useAuth();
  const [workspaces, setWorkspaces] = useState(getWorkspaceIds);
  const [workspace, setWorkspace] = useState(null);
  const [projects, setProjects] = useState([]);
  const [project, setProject] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [members, setMembers] = useState([]);
  const [page, setPage] = useState("board");
  const [search, setSearch] = useState("");
  const [priorityFilter, setPriorityFilter] = useState("");
  const [notice, setNotice] = useState("");
  const [busy, setBusy] = useState(false);
  const [dialog, setDialog] = useState("");
  const [taskToEdit, setTaskToEdit] = useState(null);
  const [projectIdInput, setProjectIdInput] = useState("");

  useEffect(() => {
    if (!user) return undefined;

    let active = true;
    setWorkspaces([]);
    setWorkspace(null);
    setProject(null);
    setProjects([]);
    setTasks([]);
    setNotice("");

    api.listWorkspaces()
      .then((items) => {
        if (!active) return;
        saveStored(WORKSPACES_KEY, items.map(({ id, name }) => ({ id, name })));
        setWorkspaces(getWorkspaceIds());
        if (items.length) loadWorkspace(items[0].id);
      })
      .catch((error) => {
        if (active) setNotice(error.message);
      });

    return () => { active = false; };
  }, [user]);

  useEffect(() => {
    if (workspace) setProjects(getProjectEntries(workspace.id));
  }, [workspace]);

  async function loadWorkspace(id, reportError = true) {
    try {
      const loaded = await api.getWorkspace(id);
      rememberWorkspace(loaded);
      setWorkspaces(getWorkspaceIds());
      setWorkspace(loaded);
      setProject(null);
      setTasks([]);
      setPage("board");
      setNotice("");
      return loaded;
    } catch (error) {
      if (reportError) setNotice(error.message);
      return null;
    }
  }

  async function selectProject(selected) {
    setProject(selected);
    setPage("board");
    setNotice("");
    setBusy(true);
    try {
      const [loadedProject, loadedTasks] = await Promise.all([
        api.getProject(selected.id),
        api.listTasks(selected.id),
      ]);
      rememberProject(loadedProject);
      setProject(loadedProject);
      setTasks(loadedTasks);
      const workspaceMembers = await api.listMembers(loadedProject.workspace_id);
      setMembers(workspaceMembers);
    } catch (error) {
      setNotice(error.message);
    } finally {
      setBusy(false);
    }
  }

  async function openTask(task) {
    setTaskToEdit(task);
    setDialog("task");
    try {
      const detailedTask = await api.getTask(task.id);
      setTaskToEdit(detailedTask);
    } catch (error) {
      setNotice(error.message);
    }
  }

  async function refreshTasks() {
    if (!project) return;
    try {
      const filters = { search: search.trim(), priority: priorityFilter };
      setTasks(await api.listTasks(project.id, filters));
    } catch (error) {
      setNotice(error.message);
    }
  }

  useEffect(() => {
    if (!project || page !== "board") return;
    const timeout = window.setTimeout(() => { refreshTasks(); }, 250);
    return () => window.clearTimeout(timeout);
  }, [search, priorityFilter, project?.id, page]);

  async function openProjectById(event) {
    event.preventDefault();
    setBusy(true);
    setNotice("");
    try {
      const loaded = await api.getProject(projectIdInput.trim());
      if (workspace && workspace.id !== loaded.workspace_id) {
        const loadedWorkspace = await loadWorkspace(loaded.workspace_id);
        if (!loadedWorkspace) return;
      }
      rememberProject(loaded);
      setProjects(getProjectEntries(loaded.workspace_id));
      setProjectIdInput("");
      await selectProject(loaded);
    } catch (error) {
      setNotice(error.message);
    } finally {
      setBusy(false);
    }
  }

  function onWorkspaceCreated(created) {
    setWorkspaces(getWorkspaceIds());
    setWorkspace(created);
    setProjects([]);
    setProject(null);
    setTasks([]);
    setPage("board");
  }

  function onProjectCreated(created) {
    setProjects(getProjectEntries(workspace.id));
    selectProject(created);
  }

  async function onTaskSaved() {
    await refreshTasks();
  }

  async function onProjectDeleted() {
    if (!project || !window.confirm("Xóa dự án này và các công việc liên quan?")) return;
    setNotice("");
    try {
      await api.deleteProject(project.id);
      saveStored(PROJECTS_KEY, readStored(PROJECTS_KEY).filter((item) => item.id !== project.id));
      setProjects(getProjectEntries(workspace.id));
      setProject(null);
      setTasks([]);
    } catch (error) {
      setNotice(error.message);
    }
  }

  const columns = useMemo(() => STATUSES.map((status) => ({
    status,
    tasks: tasks.filter((task) => task.status === status),
  })), [tasks]);

  if (loading) return <div className="full-loading"><span className="spinner" />Đang tải TaskForge...</div>;
  if (!user) return <AuthScreen />;

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand"><span className="brand-mark">T</span> TaskForge</div>
        <div className="workspace-label">WORKSPACE <button className="icon-button add-workspace" onClick={() => setDialog("workspace")} aria-label="Thêm workspace">+</button></div>
        <div className="workspace-list">
          {workspaces.map((item) => (
            <button key={item.id} className={`workspace-item${workspace?.id === item.id ? " active" : ""}`} onClick={() => loadWorkspace(item.id)}>
              <span className="workspace-icon">{initials(item.name)}</span><span className="workspace-name">{item.name}</span>
            </button>
          ))}
          {!workspaces.length && <p className="sidebar-empty">Tạo workspace hoặc mở bằng ID để bắt đầu.</p>}
        </div>
        <button className="sidebar-add" onClick={() => setDialog("workspace")}><span>＋</span> Thêm workspace</button>

        {workspace && (
          <>
            <div className="workspace-label project-label">DỰ ÁN <button className="icon-button add-workspace" onClick={() => setDialog("project")} aria-label="Tạo dự án">+</button></div>
            <nav className="project-list">
              {projects.map((item) => (
                <button key={item.id} className={`project-item${project?.id === item.id ? " active" : ""}`} onClick={() => selectProject(item)}>
                  <span className="project-key">{item.key}</span><span className="project-name">{item.name}</span>
                </button>
              ))}
              <form className="open-project-form" onSubmit={openProjectById}>
                <input value={projectIdInput} onChange={(event) => setProjectIdInput(event.target.value)} placeholder="Mở dự án bằng ID" aria-label="Project ID" />
                <button aria-label="Mở dự án" disabled={busy || !projectIdInput.trim()}>↵</button>
              </form>
              {!projects.length && <p className="sidebar-empty">Chưa có dự án đã lưu. Tạo mới hoặc mở bằng ID.</p>}
            </nav>
          </>
        )}

        <div className="sidebar-bottom">
          {workspace && <div className="side-links">
            <button className={page === "members" ? "selected" : ""} onClick={() => setPage("members")}><span>♙</span> Thành viên</button>
            <button className={page === "settings" ? "selected" : ""} onClick={() => setPage("settings")}><span>⚙</span> Cài đặt</button>
          </div>}
          <div className="user-menu">
            <div className="avatar">{initials(user.full_name)}</div>
            <div className="user-menu-info"><strong>{user.full_name}</strong><span>{user.email}</span></div>
            <button className="icon-button logout-button" onClick={logout} title="Đăng xuất" aria-label="Đăng xuất">↗</button>
          </div>
        </div>
      </aside>

      <main className="main-area">
        <header className="topbar">
          <div className="breadcrumbs"><span>{workspace?.name || "Không gian làm việc"}</span>{project && <><b>/</b><strong>{project.name}</strong></>}</div>
          {workspace && project && <div className="topbar-actions">
            <button className="button secondary" onClick={() => setDialog("edit-project")}>Sửa dự án</button>
            <button className="button secondary" onClick={onProjectDeleted}>Xóa dự án</button>
            <button className="button primary" onClick={() => { setTaskToEdit(null); setDialog("task"); }}>＋ Tạo công việc</button>
          </div>}
        </header>
        {notice && <div className="global-notice"><ErrorMessage>{notice}</ErrorMessage><button className="icon-button" onClick={() => setNotice("")} aria-label="Đóng thông báo">×</button></div>}

        {!workspace ? (
          <section className="welcome-state">
            <div className="welcome-icon">✦</div><p className="eyebrow">CHÀO MỪNG ĐẾN TASKFORGE</p>
            <h1>Bắt đầu với một<br />không gian làm việc.</h1>
            <p className="muted">Tạo workspace mới hoặc mở workspace có sẵn bằng ID.</p>
            <button className="button primary" onClick={() => setDialog("workspace")}>＋ Tạo hoặc mở workspace</button>
          </section>
        ) : page === "members" ? (
          <MembersView workspace={workspace} onError={setNotice} />
        ) : page === "settings" ? (
          <SettingsView workspace={workspace} user={user} onWorkspaceUpdated={(updated) => { setWorkspace(updated); setWorkspaces(getWorkspaceIds()); }} onWorkspaceDeleted={(id) => {
            saveStored(WORKSPACES_KEY, getWorkspaceIds().filter((item) => item.id !== id));
            saveStored(PROJECTS_KEY, readStored(PROJECTS_KEY).filter((item) => item.workspaceId !== id));
            setWorkspaces(getWorkspaceIds()); setWorkspace(null); setProject(null); setProjects([]); setTasks([]);
          }} onProfileUpdated={setUser} onError={setNotice} />
        ) : !project ? (
          <section className="welcome-state project-welcome">
            <div className="welcome-icon">▧</div><p className="eyebrow">{workspace.name.toUpperCase()}</p>
            <h1>Chọn một dự án<br />để xem công việc.</h1>
            <p className="muted">Bạn có thể tạo dự án hoặc mở một dự án bằng ID.</p>
            <button className="button primary" onClick={() => setDialog("project")}>＋ Tạo dự án</button>
            <p className="field-hint">Backend chưa cung cấp API danh sách dự án; các dự án đã tạo trên thiết bị này được lưu lại tại đây.</p>
          </section>
        ) : (
          <section className="board-page">
            <div className="board-heading">
              <div><p className="eyebrow">{workspace.name} <span className="crumb-dot">•</span> {project.key}</p><h1>{project.name}</h1><p className="muted">{project.description || "Theo dõi và quản lý công việc của dự án."}</p></div>
              <div className="project-avatar">{project.key.slice(0, 2)}</div>
            </div>
            <div className="board-toolbar">
              <div className="search-field"><span>⌕</span><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Tìm công việc..." /></div>
              <select value={priorityFilter} onChange={(event) => setPriorityFilter(event.target.value)} aria-label="Lọc theo độ ưu tiên">
                <option value="">Mọi độ ưu tiên</option>{PRIORITIES.map((value) => <option key={value} value={value}>{PRIORITY_LABELS[value]}</option>)}
              </select>
              <span className="task-count">{tasks.length} công việc</span>
            </div>
            {busy ? <div className="loading-state"><span className="spinner" />Đang tải dữ liệu...</div> : (
              <div className="board">
                {columns.map(({ status, tasks: statusTasks }) => (
                  <section className="board-column" key={status}>
                    <div className="column-heading"><span className={`status-dot status-${status.toLowerCase()}`} /><h2>{STATUS_LABELS[status]}</h2><span className="column-count">{statusTasks.length}</span><button className="column-add" onClick={() => { setTaskToEdit(null); setDialog("task"); }}>＋</button></div>
                    <div className="column-cards">
                      {statusTasks.map((task) => <TaskCard key={task.id} task={task} onClick={() => openTask(task)} />)}
                      {!statusTasks.length && <div className="column-empty">Chưa có công việc</div>}
                      {status === "TODO" && <button className="add-task-inline" onClick={() => { setTaskToEdit(null); setDialog("task"); }}>＋ Tạo công việc</button>}
                    </div>
                  </section>
                ))}
              </div>
            )}
          </section>
        )}
      </main>

      {dialog === "workspace" && <WorkspaceDialog onClose={() => setDialog("")} onCreated={onWorkspaceCreated} />}
      {dialog === "project" && workspace && <ProjectDialog workspace={workspace} onClose={() => setDialog("")} onCreated={onProjectCreated} />}
      {dialog === "edit-project" && project && <EditProjectDialog project={project} onClose={() => setDialog("")} onSaved={(updated) => { setProject(updated); setProjects(getProjectEntries(updated.workspace_id)); }} />}
      {dialog === "task" && project && <TaskDialog project={project} task={taskToEdit} members={members} onClose={() => setDialog("")} onSaved={onTaskSaved} onDeleted={(id) => setTasks((current) => current.filter((item) => item.id !== id))} />}
    </div>
  );
}

export default App;
