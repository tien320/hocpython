Trong Git, đây là **4 khu vực lưu trữ chính** thể hiện vòng đời của mã nguồn từ lúc bạn bắt đầu viết cho đến khi được đồng bộ lên máy chủ.

```text
[Working Directory] --(git add)--> [Staging Area] --(git commit)--> [Local Repository] --(git push)--> [Remote Repository]

```

---

### 1. Working Directory (Thư mục làm việc)

- **Khái niệm:** Là thư mục thực tế trên ổ cứng máy tính nơi bạn mở code, tạo file, chỉnh sửa nội dung hoặc xóa file.
- **Đặc điểm:** Các thay đổi ở đây chưa được Git theo dõi để đóng gói thành phiên bản lưu trữ. Nếu bạn sửa sai hoặc lỡ xóa file mà chưa lưu vào Git, dữ liệu có thể bị mất hoàn toàn.
- **Lệnh liên quan:** `git status` (hiển thị file đã sửa nhưng chưa add).

### 2. Staging Area (Khu vực chuẩn bị / Index)

- **Khái niệm:** Vùng đệm tạm thời chứa danh sách các thay đổi mà bạn dự định sẽ đưa vào lần commit tiếp theo.
- **Đặc điểm:** Giúp bạn chọn lọc chính xác những file hoặc dòng code nào sẵn sàng để lưu lại thành một phiên bản. Bạn có thể sửa 5 file trong Working Directory nhưng chỉ chọn 2 file đưa vào Staging Area.
- **Lệnh liên quan:**
- `git add <tên_file>` (đưa file vào Staging)
- `git restore --staged <tên_file>` (rút file ra khỏi Staging về lại Working Directory)

### 3. Local Repository (Kho lưu trữ cục bộ)

- **Khái niệm:** Toàn bộ lịch sử commit, các nhánh (branch) và metadata được lưu trong thư mục ẩn `.git` ngay trên máy bạn.
- **Đặc điểm:** Khi commit thành công, thay đổi chính thức trở thành một bản snapshot an toàn có mã băm (commit hash). Bạn có thể quay lại phiên bản này bất cứ lúc nào ngay cả khi không có kết nối internet.
- **Lệnh liên quan:**
- `git commit -m "nội dung"` (đóng gói từ Staging Area vào Local Repo)
- `git log` (xem lịch sử commit)

### 4. Remote Repository (Kho lưu trữ từ xa)

- **Khái niệm:** Kho lưu trữ nằm trên máy chủ hoặc các dịch vụ đám mây như GitHub, GitLab, Bitbucket.
- **Đặc điểm:** Dùng để sao lưu trực tuyến và phối hợp làm việc nhóm. Các lập trình viên trong đội dự án sẽ đẩy (push) code của mình lên đây và kéo (pull) code của người khác về.
- **Lệnh liên quan:**
- `git push origin <tên_nhánh>` (đẩy commit từ Local Repo lên Remote Repo)
- `git pull origin <tên_nhánh>` (lấy thay đổi mới nhất từ Remote Repo về Local và merge vào Working Directory)

---

### Bảng tóm tắt so sánh

| Khu vực               | Vị trí lưu trữ                   | Trạng thái dữ liệu               | Thao tác chính đưa dữ liệu vào |
| --------------------- | -------------------------------- | -------------------------------- | ------------------------------ |
| **Working Directory** | Ổ đĩa máy bạn (file thật)        | Đang chỉnh sửa, chưa chốt        | Code trực tiếp trên IDE/Editor |
| **Staging Area**      | Bộ nhớ đệm trong `.git`          | Đã chọn lọc, sẵn sàng commit     | `git add`                      |
| **Local Repository**  | Thư mục `.git` trên máy bạn      | Đã đóng gói thành lịch sử cục bộ | `git commit`                   |
| **Remote Repository** | Máy chủ mạng (GitHub, GitLab...) | Lưu trữ tập trung cho cả nhóm    | `git push`                     |
