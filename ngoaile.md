Khi làm việc với File (I/O Operations), chương trình của bạn phải giao tiếp với môi trường bên ngoài (ổ cứng, hệ điều hành). Do đó, đây là nơi **rất dễ xảy ra lỗi** nằm ngoài tầm kiểm soát của code (file không tồn tại, ổ cứng bị khóa, bị ngắt quyền truy cập, file rác không đúng định dạng...).

Để chương trình không bị **crash (sập)** đột ngột, chúng ta sử dụng cơ chế **Xử lý ngoại lệ (Exception Handling)** với khối `try...except...else...finally`.

---

## 1. Cấu trúc tổng quát của khối Xử lý ngoại lệ

```python
try:
    # [1] Đoạn code CÓ THỂ gây ra lỗi khi thao tác với File
    file = open('data.json', mode='r', encoding='utf-8')
    data = json.load(file)

except FileNotFoundError:
    # [2] Chạy khi KHÔNG TÌM THẤY FILE
    print("Lỗi: File bạn cần đọc không tồn tại trên ổ cứng!")

except json.JSONDecodeError:
    # [3] Chạy khi FILE BỊ LỖI ĐỊNH DẠNG (ví dụ file JSON bị mất dấu } hoặc hỏng)
    print("Lỗi: Nội dung file JSON bị hỏng, không đúng cú pháp!")

except Exception as e:
    # [4] Catch-all: Chạy khi gặp BẤT KỲ LỖI NÀO KHÁC chưa lường trước được
    print(f"Đã xảy ra lỗi hệ thống bất ngờ: {e}")

else:
    # [5] (Tùy chọn) CHỈ CHẠY khi khối `try` thực thi THÀNH CÔNG (Không có lỗi nào)
    print("Đọc file thành công! Số lượng bản ghi:", len(data))

finally:
    # [6] LUÔN LUÔN CHẠY dù có lỗi hay không (Thường dùng để dọn dẹp tài nguyên)
    print("Hoàn tất tiến trình thao tác với file.")

```

---

## 2. Các ngoại lệ (Exceptions) thường gặp nhất khi làm việc với File

Khi thao tác I/O, Python định nghĩa sẵn các loại ngoại lệ phổ biến sau:

| Tên Exception              | Nguyên nhân xảy ra                        | Ví dụ thực tế                                                                      |
| -------------------------- | ----------------------------------------- | ---------------------------------------------------------------------------------- |
| **`FileNotFoundError`**    | Đường dẫn file không tồn tại.             | Mở file `data.csv` nhưng quên chưa tạo file.                                       |
| **`PermissionError`**      | Không có quyền đọc/ghi file.              | Ghi đè vào file hệ thống Windows (`C:\Windows\...`) hoặc file đang mở trong Excel. |
| **`UnicodeDecodeError`**   | Lỗi sai bảng mã mã hóa (`encoding`).      | Mở file lưu dạng ANSI/CP1252 bằng `encoding='utf-8'`.                              |
| **`json.JSONDecodeError`** | File JSON bị sai cú pháp.                 | Dữ liệu JSON bị thừa dấu phẩy, thiếu ngoặc `}` hoặc bị trống file.                 |
| **`csv.Error`**            | File CSV bị lỗi khi phân tích cú pháp.    | File CSV có định dạng quá phức tạp hoặc bị ngắt ngang giữa chừng.                  |
| **`IsADirectoryError`**    | Đường dẫn trỏ tới 1 Thư mục thay vì File. | Gọi `open('my_folder/', 'r')`.                                                     |

---

## 3. Kiến thức nền & Sâu: Tại sao phải xử lý lỗi thế này?

### 3.1. Mối quan hệ giữa `try...finally` và `with open(...)`

Ở bài trước, bạn đã học câu lệnh `with open(...) as f:`. Vậy mối quan hệ của nó với `try...finally` là gì?

- **Bản chất của `with`:** Bản thân `with` là một cú pháp viết tắt (Syntactic Sugar) của khối `try...finally` để **tự động đóng File Stream**.
- **So sánh 2 cách viết có giá trị tương đương:**

:::code-group

```python [Cách 1: Dùng try...finally thủ công]
file = None
try:
    file = open('data.txt', 'r', encoding='utf-8')
    content = file.read()
except FileNotFoundError:
    print("File không tồn tại!")
finally:
    # Bắt buộc đóng file kể cả khi hàm read() bị sập
    if file and not file.closed:
        file.close()

```

```python [Cách 2: Dùng với with (Khuyên dùng)]
try:
    with open('data.txt', 'r', encoding='utf-8') as file:
        content = file.read()
except FileNotFoundError:
    print("File không tồn tại!")
# 'with' đã tự động thực hiện đoạn code file.close() ở cuối cho bạn!

```

:::

> **💡 Best Practice:** Luôn lồng `with open(...)` **bên trong** khối `try...except`. Bằng cách này: `with` sẽ lo việc đóng file an toàn, còn `except` sẽ lo việc hứng các lỗi phát sinh.

---

### 3.2. Tại sao KHÔNG NÊN dùng `except Exception:` duy nhất cho tất cả?

```python
# ❌ LẮP LỖI BẮT TỰ ĐỘNG - BAD PRACTICE:
try:
    with open('data.json', 'r') as f:
        data = json.load(f)
except Exception:
    print("Đã có lỗi xảy ra!") # 👈 Người dùng không biết chính xác lỗi gì!

```

- **Tại sao không nên?** Bạn giấu đi nguyên nhân gốc rễ (Root Cause). File bị thiếu? Hay file bị hỏng? Hay do lỗi thiếu bộ nhớ RAM? Tất cả đều bị gom chung vào một câu thông báo mơ hồ.
- **Cách viết chuẩn (Explicit Exception Handling):** Phân tách rõ ràng từng loại Exception từ **Cụ thể đến Tổng quát** (từ con đến cha).

---

## 4. Code mẫu chuẩn Doanh nghiệp (Production-Ready)

Dưới đây là một hàm đọc file JSON hoàn chỉnh áp dụng đầy đủ kiến thức xử lý ngoại lệ chuẩn hóa, an toàn cho hệ thống lớn:

```python
import json
import logging

def doc_file_json_an_toan(duong_dan_file):
    """
    Hàm đọc file JSON an toàn, không làm sập chương trình.
    Trả về Dict/List nếu thành công, trả về None nếu thất bại.
    """
    try:
        with open(duong_dan_file, mode='r', encoding='utf-8') as f:
            data = json.load(f)
            return data

    except FileNotFoundError:
        logging.error(f"[X] Lỗi: Không tìm thấy file tại đường dẫn: '{duong_dan_file}'")

    except PermissionError:
        logging.error(f"[X] Lỗi: Không có quyền truy cập/đọc file: '{duong_dan_file}'")

    except json.JSONDecodeError as e:
        logging.error(f"[X] Lỗi: File JSON bị sai định dạng tại dòng {e.lineno}, cột {e.colno}")

    except UnicodeDecodeError:
        logging.error(f"[X] Lỗi: Sai bảng mã (Encoding). Hãy kiểm tra xem file có phải UTF-8 không.")

    except Exception as e:
        logging.error(f"[X] Lỗi không xác định: {type(e).__name__} - {e}")

    # Nếu chạy xuống đây nghĩa là đã nhảy vào một trong các khối except ở trên
    return None

# === THỬ NGHIỆM HÀM ===
# Test 1: Đọc file không tồn tại
ket_qua = doc_file_json_an_toan("file_khong_co_that.json")
# Output: [X] Lỗi: Không tìm thấy file tại đường dẫn: 'file_khong_co_that.json'

if ket_qua is not None:
    print("Xử lý dữ liệu tiếp...")
else:
    print("Dùng dữ liệu mặc định để chạy tiếp chương trình mà không bị crash.")

```

---

## 5. Giá trị mang lại cho hệ thống

1. **Khả năng Phục hồi Lỗi (Fault Tolerance):** Nếu chương trình là một Server chạy 24/7, việc một người dùng tải lên file CSV bị lỗi sẽ không làm crash toàn bộ Server. Hệ thống chỉ bắt lỗi file đó, bỏ qua và tiếp tục phục vụ các người dùng khác.
2. **Ghi vết Lỗi (Debugging / Logging):** Bắt đúng loại `Exception` giúp bạn in ra dòng bị lỗi (`e.lineno`), lý do bị lỗi để ghi vào hệ thống Log, giúp Kỹ sư phần mềm tìm ra bug và sửa chỉ trong vài phút.
3. **Thân thiện với người dùng:** Thay vì hiện ra màn hình một dải Traceback màu đỏ hù dọa người dùng, bạn có thể thông báo nhẹ nhàng: _"File bạn tải lên không đúng định dạng, vui lòng kiểm tra lại!"_.
