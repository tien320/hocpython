Dưới đây là danh sách đầy đủ các RESTful API endpoints cần xây dựng cho hệ thống **TaskForge**, được chuẩn hóa theo chuẩn REST, phân tầng tài nguyên và gắn kèm logic phân quyền.

---

### 1. Authentication (`/api/v1/auth`)

| Phương thức | Endpoint                | Quyền truy cập | Mô tả & Chức năng                                         |
| ----------- | ----------------------- | -------------- | --------------------------------------------------------- |
| `POST`      | `/api/v1/auth/register` | Public         | Đăng ký tài khoản mới (`email`, `password`, `full_name`). |
| `POST`      | `/api/v1/auth/login`    | Public         | Đăng nhập và nhận về `access_token` (JWT).                |
| `GET`       | `/api/v1/auth/me`       | Authenticated  | Lấy thông tin tài khoản hiện tại từ JWT.                  |

---

### 2. Workspaces (`/api/v1/workspaces`)

| Phương thức     | Endpoint                          | Quyền truy cập   | Mô tả & Chức năng                                   |
| --------------- | --------------------------------- | ---------------- | --------------------------------------------------- |
| `POST`          | `/api/v1/workspaces`              | Authenticated    | Tạo workspace mới (User tạo tự động thành `OWNER`). |
| `GET`           | `/api/v1/workspaces`              | Authenticated    | Lấy danh sách các workspace mà user đang tham gia.  |
| `GET`           | `/api/v1/workspaces/:workspaceId` | Workspace Member | Xem thông tin chi tiết một workspace.               |
| `PUT` / `PATCH` | `/api/v1/workspaces/:workspaceId` | Owner / Admin    | Cập nhật thông tin workspace (tên, slug).           |
| `DELETE`        | `/api/v1/workspaces/:workspaceId` | Owner            | Xóa workspace.                                      |

---

### 3. Workspace Members (`/api/v1/workspaces/:workspaceId/members`)

| Phương thức | Endpoint                                          | Quyền truy cập   | Mô tả & Chức năng                                              |
| ----------- | ------------------------------------------------- | ---------------- | -------------------------------------------------------------- |
| `GET`       | `/api/v1/workspaces/:workspaceId/members`         | Workspace Member | Danh sách thành viên trong workspace.                          |
| `POST`      | `/api/v1/workspaces/:workspaceId/members`         | Owner / Admin    | Thêm thành viên mới vào workspace (`user_id`/`email`, `role`). |
| `PATCH`     | `/api/v1/workspaces/:workspaceId/members/:userId` | Owner / Admin    | Cập nhật vai trò (`role`) của thành viên (`ADMIN`, `MEMBER`).  |
| `DELETE`    | `/api/v1/workspaces/:workspaceId/members/:userId` | Owner / Admin    | Xóa thành viên khỏi workspace (hoặc user tự rời).              |

---

### 4. Projects (`/api/v1/workspaces/:workspaceId/projects`)

| Phương thức     | Endpoint                                   | Quyền truy cập          | Mô tả & Chức năng                        |
| --------------- | ------------------------------------------ | ----------------------- | ---------------------------------------- |
| `POST`          | `/api/v1/workspaces/:workspaceId/projects` | Workspace Member        | Tạo dự án mới bên trong workspace.       |
| `GET`           | `/api/v1/workspaces/:workspaceId/projects` | Workspace Member        | Lấy danh sách các dự án trong workspace. |
| `GET`           | `/api/v1/projects/:projectId`              | Workspace Member        | Lấy thông tin chi tiết một dự án.        |
| `PUT` / `PATCH` | `/api/v1/projects/:projectId`              | Project Creator / Admin | Cập nhật thông tin dự án (tên, mô tả).   |
| `DELETE`        | `/api/v1/projects/:projectId`              | Owner / Admin           | Xóa một dự án.                           |

---

### 5. Tasks / Issues (`/api/v1/projects/:projectId/tasks` & `/api/v1/tasks`)

| Phương thức     | Endpoint                            | Quyền truy cập       | Mô tả & Chức năng                                                                                                    |
| --------------- | ----------------------------------- | -------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `POST`          | `/api/v1/projects/:projectId/tasks` | Workspace Member     | Tạo task mới (`title`, `description`, `priority`, `assignee_id`).                                                    |
| `GET`           | `/api/v1/projects/:projectId/tasks` | Workspace Member     | **List & Filter Task:** Lọc theo `status`, `priority`, `assignee_id`, `search` từ khóa, phân trang `page` & `limit`. |
| `GET`           | `/api/v1/tasks/:taskId`             | Workspace Member     | Xem chi tiết thông tin task.                                                                                         |
| `PUT` / `PATCH` | `/api/v1/tasks/:taskId`             | Workspace Member     | Cập nhật thông tin chung của task.                                                                                   |
| `PATCH`         | `/api/v1/tasks/:taskId/status`      | Workspace Member     | Cập nhật riêng trạng thái task (`TODO`, `IN_PROGRESS`, `DONE`...).                                                   |
| `PATCH`         | `/api/v1/tasks/:taskId/assignee`    | Workspace Member     | Gán hoặc đổi người thực hiện task (`assignee_id` hoặc `null`).                                                       |
| `DELETE`        | `/api/v1/tasks/:taskId`             | Task Creator / Admin | Xóa task.                                                                                                            |

---

### 6. Comments (`/api/v1/tasks/:taskId/comments`)

| Phương thức | Endpoint                         | Quyền truy cập   | Mô tả & Chức năng                            |
| ----------- | -------------------------------- | ---------------- | -------------------------------------------- |
| `GET`       | `/api/v1/tasks/:taskId/comments` | Workspace Member | Lấy danh sách bình luận của một task.        |
| `POST`      | `/api/v1/tasks/:taskId/comments` | Workspace Member | Viết bình luận mới vào task (`content`).     |
| `PATCH`     | `/api/v1/comments/:commentId`    | Comment Author   | Chỉnh sửa nội dung bình luận của chính mình. |
| `DELETE`    | `/api/v1/comments/:commentId`    | Author / Admin   | Xóa bình luận.                               |
