Các nhóm mã 1xx, 2xx và 3xx hoàn thiện bức tranh toàn bộ chu trình xử lý của giao thức HTTP, đại diện cho quá trình khởi tạo, thành công và chuyển hướng.

---

### 1xx (Informational - Thông tin)

Thông báo yêu cầu đã được tiếp nhận và quá trình xử lý vẫn đang tiếp tục; client không cần gửi lại request.

| Mã      | Tên                     | Ý nghĩa                                                                                                                |
| ------- | ----------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **100** | **Continue**            | Server đã nhận phần đầu (headers) của request, client tiếp tục gửi phần thân (body).                                   |
| **101** | **Switching Protocols** | Server đồng ý chuyển giao thức (thường gặp khi nâng cấp từ HTTP lên **WebSocket**).                                    |
| **103** | **Early Hints**         | Server trả trước một số link tài nguyên (CSS, JS) để trình duyệt preload trong lúc chờ server tạo nội dung HTML chính. |

---

### 2xx (Success - Thành công)

Yêu cầu đã được server tiếp nhận, hiểu và xử lý thành công.

| Mã      | Tên                 | Ý nghĩa & Khi nào dùng                                                                                                                     |
| ------- | ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **200** | **OK**              | Request thành công chuẩn (thường dùng cho `GET`, `PUT`, `PATCH`).                                                                          |
| **201** | **Created**         | Tạo mới tài nguyên thành công (chuẩn mực cho phương thức `POST`). Server thường trả về URL của tài nguyên vừa tạo trong header `Location`. |
| **202** | **Accepted**        | Server đã nhận request nhưng đưa vào hàng đợi xử lý ngầm (asynchronous/background job), chưa hoàn tất ngay.                                |
| **204** | **No Content**      | Xử lý thành công nhưng **không trả về dữ liệu trong body** (rất phổ biến cho request `DELETE` hoặc `OPTIONS`).                             |
| **206** | **Partial Content** | Trả về một phần dữ liệu (khi client tải file ngắt quãng hoặc xem video streaming có header `Range`).                                       |

---

### 3xx (Redirection - Chuyển hướng)

Client cần thực hiện thêm hành động bổ sung (thường là đổi URL) để hoàn tất yêu cầu.

| Mã      | Tên                            | Ý nghĩa & Ứng dụng                                                                                                                                 |
| ------- | ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| **301** | **Moved Permanently**          | Tài nguyên đã chuyển vĩnh viễn sang URL mới. Trình duyệt và bot tìm kiếm (SEO) sẽ cập nhật và lưu cache URL mới này.                               |
| **302** | **Found (Temporary Redirect)** | Chuyển hướng tạm thời. Không đổi URL gốc trong SEO, dùng khi bảo trì trang hoặc điều hướng thanh toán.                                             |
| **304** | **Not Modified**               | Dùng cho **Browser Cache**. Server báo tài nguyên chưa thay đổi kể từ lần tải trước; client lấy trực tiếp từ bộ nhớ đệm mà không cần tải lại file. |
| **307** | **Temporary Redirect**         | Tương tự 302, nhưng **bắt buộc giữ nguyên phương thức HTTP** (nếu gửi `POST` ban đầu thì sau chuyển hướng vẫn phải là `POST`).                     |
| **308** | **Permanent Redirect**         | Tương tự 301, nhưng **bắt buộc giữ nguyên phương thức HTTP** như lúc đầu.                                                                          |

---

### Có mã 6xx hay 7xx không?

Theo tiêu chuẩn chính thức của **IETF (RFC 9110)**: **Hoàn toàn KHÔNG có mã 6xx hay 7xx.**

- Chuẩn HTTP chỉ định nghĩa phạm vi 3 chữ số từ **100 đến 599**:
- `1xx`: Informational
- `2xx`: Successful
- `3xx`: Redirection
- `4xx`: Client Error
- `5xx`: Server Error

- Bất kỳ mã nào $\ge 600$ đều vi phạm đặc tả kỹ thuật HTTP chuẩn.

#### Một số trường hợp ngoại lệ bên ngoài chuẩn:

1. **Dự án đùa cợt (Joke RFC/Satire):** Cộng đồng lập trình viên có một dự án mã nguồn mở trào phúng gọi là _"7xx Developer Errors"_ (ví dụ: `701 - Cheapskate`, `720 - Unhandled Exception`). Đây chỉ là nội dung hài hước của giới developer, không thể hoạt động trên Internet.
2. **Hệ thống nội bộ tùy biến (Non-standard):** Một số công ty hoặc proxy tùy chỉnh tự định nghĩa mã riêng trong mạng nội bộ (như SMTP/SIP dùng các dải mã số khác với HTTP). Tuy nhiên, trên web công khai, trình duyệt và các thư viện HTTP client chuẩn sẽ xem bất kỳ mã nào ngoài dải 100–599 là không hợp lệ.
