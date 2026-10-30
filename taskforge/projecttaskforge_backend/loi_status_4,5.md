Mã trạng thái HTTP (HTTP status code) là các số gồm 3 chữ số do máy chủ (server) phản hồi về cho client (trình duyệt, ứng dụng) để thông báo kết quả của một request. Trong đó, **các mã biểu thị lỗi thuộc hai nhóm chính**:

- **Nhóm 4xx (Client Errors):** Lỗi xuất phát từ phía người gửi request (sai cú pháp, thiếu xác thực, tài nguyên không tồn tại...).
- **Nhóm 5xx (Server Errors):** Lỗi xuất phát từ phía máy chủ (sập server, quá tải, lỗi cấu hình gateway...).

---

### Các mã lỗi 4xx phổ biến (Lỗi Client)

| Mã lỗi  | Tên mã                   | Ý nghĩa & Nguyên nhân thường gặp                                                                                                  |
| ------- | ------------------------ | --------------------------------------------------------------------------------------------------------------------------------- |
| **400** | **Bad Request**          | Server không hiểu request do sai cú pháp (sai định dạng JSON, thiếu tham số bắt buộc, header không hợp lệ).                       |
| **401** | **Unauthorized**         | Cần xác thực danh tính để truy cập nhưng client chưa đăng nhập hoặc token/cookie đã hết hạn.                                      |
| **403** | **Forbidden**            | Server đã xác thực danh tính nhưng client **không có quyền** truy cập tài nguyên đó (ví dụ: tài khoản thường cố vào trang admin). |
| **404** | **Not Found**            | Tài nguyên (URL, API endpoint, file) không tồn tại trên hệ thống hoặc đã bị xóa.                                                  |
| **405** | **Method Not Allowed**   | Phương thức HTTP không được hỗ trợ tại endpoint này (ví dụ: API chỉ nhận `POST` nhưng client lại gửi `GET`).                      |
| **408** | **Request Timeout**      | Máy chủ hết thời gian chờ request từ client (thường do kết nối mạng chập chờn).                                                   |
| **409** | **Conflict**             | Xảy ra xung đột với trạng thái hiện tại của server (ví dụ: tạo tài khoản với email đã được đăng ký trước đó).                     |
| **422** | **Unprocessable Entity** | Cú pháp request đúng chuẩn nhưng dữ liệu bên trong không hợp lệ (ví dụ: sai kiểu dữ liệu trường trong body, vi phạm validation).  |
| **429** | **Too Many Requests**    | Client gửi quá nhiều request trong một khoảng thời gian, chạm giới hạn Rate Limit của server.                                     |

---

### Các mã lỗi 5xx phổ biến (Lỗi Server)

| Mã lỗi  | Tên mã                    | Ý nghĩa & Nguyên nhân thường gặp                                                                                                  |
| ------- | ------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| **500** | **Internal Server Error** | Lỗi chung của server; mã nguồn backend gặp lỗi ngoại lệ (exception, crash, lỗi kết nối database) mà không được xử lý (try/catch). |
| **502** | **Bad Gateway**           | Máy chủ đóng vai trò Gateway/Proxy (như Nginx, Cloudflare) nhận phản hồi không hợp lệ từ máy chủ backend phía sau.                |
| **503** | **Service Unavailable**   | Server hiện không thể phục vụ do đang bảo trì hoặc bị quá tải lưu lượng đột ngột (DDoS, lưu lượng tăng vọt).                      |
| **504** | **Gateway Timeout**       | Gateway/Proxy gửi request đến server backend nhưng backend xử lý quá lâu, vượt quá thời gian timeout quy định.                    |

---

### Cách phân biệt nhanh hai cặp lỗi dễ nhầm lẫn

- **401 vs 403:**
- `401 Unauthorized` = _"Bạn là ai? Tôi chưa biết danh tính của bạn."_ (Chưa đăng nhập/Token sai).
- `403 Forbidden` = _"Tôi biết bạn là ai, nhưng bạn không có quyền vào đây."_ (Đã đăng nhập nhưng thiếu quyền).

- **502 vs 504:**
- `502 Bad Gateway` = Gateway nhận được câu trả lời **sai/lỗi** từ backend.
- `504 Gateway Timeout` = Gateway **chờ mãi không thấy** backend trả lời.
