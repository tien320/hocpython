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
   Để hiểu trọn vẹn về **Xử lý ngoại lệ (Exception Handling)**, chúng ta cần quay ngược thời gian về thời kỳ lập trình sơ khai để thấy lý do các kỹ sư máy tính phải phát minh ra cơ chế này, bản chất bên dưới hệ thống (Kernel/CPU) vận hành ra sao và giá trị cốt lõi nó mang lại.

---

## 1. Lịch sử & Bối cảnh: Khi Xử lý ngoại lệ chưa ra đời

Trước khi cơ chế `try-except` ra đời (thời ngôn ngữ C/Assembly), lập trình viên phải xử lý lỗi bằng cách **kiểm tra Mã trả về (Return Code)** sau mỗi dòng lệnh.

### Code thời chưa có `try-except` (Viết bằng C):

```c
FILE *f = fopen("data.txt", "r");
if (f == NULL) {
    // Xử lý lỗi không mở được file
    return ERROR_FILE_NOT_FOUND;
}

int status = read_data(f);
if (status != SUCCESS) {
    // Xử lý lỗi không đọc được file
    fclose(f);
    return ERROR_READ_FAILED;
}
fclose(f);

```

### ❌ 3 Nhược điểm chết người của cách làm cũ:

1. **Trộn lẫn Logic chính và Logic xử lý lỗi:** Code chạy thực tế chỉ có 2 dòng (`open` và `read`), nhưng code kiểm tra lỗi chiếm tới 80% dung lượng. Code bị rối rắm và rất khó đọc (người ta gọi đây là hiện tượng _Spaghetti Error Handling_).
2. **Dễ bị bỏ quên lỗi:** Lập trình viên rất dễ "quên" viết lệnh `if (status != SUCCESS)`, dẫn đến việc chương trình tiếp tục chạy với dữ liệu bị rác mà không ai hay biết.
3. **Không thể "chuyển giao" lỗi lên tầng trên:** Nếu một hàm nằm sâu ở tầng 10 bị lỗi, nó phải trả về mã lỗi qua lần lượt 9 hàm phía trên nó để đến được nơi cần xử lý.

$\rightarrow$ **Sự ra đời của Exception Handling:** Nhằm tách rời hoàn toàn **"Luồng chạy chuẩn (Happy Path)"** ra khỏi **"Luồng xử lý sự cố (Error Path)"**.

---

## 2. Bản chất bên dưới: Hệ điều hành & CPU xử lý Exception như thế nào?

Khi một dòng code bị lỗi (ví dụ: chia cho 0, hoặc đọc file không tồn tại), về mặt bản chất phần cứng:

1. **Tín hiệu ngắt từ Hệ điều hành (OS Trap/Interrupt):**
   Khi bạn gọi `open()` một file không tồn tại, OS Kernel sẽ không thể tìm thấy Sector chứa file trên ổ cứng. Kernel phát ra một **Tín hiệu ngắt (Signal/Interrupt)** gửi tới Tiến trình (Process) Python đang chạy.
2. **Tạo đối tượng Ngoại lệ (Exception Object):**
   Nhân Python (Python Interpreter) nhận tín hiệu từ OS. Nó ngay lập tức đóng đóng gói toàn bộ thông tin sự cố thành một **Đối tượng (Object)** trên RAM. Đối tượng này chứa:

- **Loại lỗi** (ví dụ: `FileNotFoundError`).
- **Thông điệp lỗi** (Error Message).
- **Dấu vết Call Stack (Traceback):** Tên file, tên hàm, số thứ tự dòng code gây ra lỗi.

3. **Cơ chế Lan truyền Lỗi (Stack Unwinding):**
   Python sẽ dừng ngay lập tức luồng chạy hiện tại và **"quăng" (throw/raise)** đối tượng lỗi này ngược lên danh sách các hàm đang gọi nó (Call Stack):

- Nếu hàm hiện tại có khối `try...except` khớp với loại lỗi đó $\rightarrow$ Bắt lấy (Catch) và xử lý.
- Nếu hàm hiện tại không có $\rightarrow$ Thoát khỏi hàm đó, nhảy ngược lên hàm cha đã gọi nó.
- Nếu nhảy ngược lên tận cùng (Hàm `main`) mà vẫn không ai chịu bắt $\rightarrow$ Python mới chấp nhận **Sập chương trình (Crash)** và in bảng Traceback ra màn hình.

```
[Nhân Python phát hiện lỗi]
        │
        ▼
   Có khối try...except không?
     ├── CÓ  ──> Chạy code trong except (Hệ thống an toàn!)
     └── KHÔNG ─> Thoát hàm hiện tại, nhảy lên Hàm cha (Stack Unwinding)
                        │
                        ▼
            Hàm cha có except không?
              ├── CÓ  ──> Chạy code trong except
              └── KHÔNG ─> Tiếp tục nhảy lên... đến khi CRASH!

```

---

## 3. So sánh Kiến trúc: Code thường vs. Code dùng Exception

| Tiêu chí           | Kiểm tra lỗi kiểu cũ (`if/else`)             | Xử lý ngoại lệ (`try/except`)                                                                  |
| ------------------ | -------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| **Tách biệt Code** | Trộn lẫn logic chạy chính và logic bắt lỗi.  | **Tách biệt hoàn toàn:** Tất cả code chạy chính nằm ở `try`, tất cả xử lý lỗi gom về `except`. |
| **Lan truyền lỗi** | Phải tự truyền mã lỗi thủ công qua từng hàm. | **Tự động lan truyền (Stack Unwinding)** lên tầng nào đủ khả năng xử lý.                       |
| **Rủi ro bỏ sót**  | Dễ bỏ quên nếu không viết `if`.              | **Bắt buộc phải xử lý**, nếu không xử lý hệ thống sẽ dừng để tránh làm sai lệch dữ liệu.       |

---

## 4. Giá trị thực sự mà Exception mang lại

### 1. Giữ cho Hệ thống không bị "Sập dây chuyền" (Fault Tolerance)

Trong một ứng dụng Web (như Facebook hay Shopee), có hàng triệu người dùng cùng lúc. Nếu 1 người dùng tải lên một file CSV bị hỏng:

- **Không có Exception:** Server bị Crash $\rightarrow$ Toàn bộ trang web sập $\rightarrow$ Tất cả người dùng khác bị văng ra.
- **Có Exception:** Khối `try-except` bắt riêng lỗi của người dùng đó, gửi thông báo _"File hỏng"_ $\rightarrow$ Server vẫn sống bình thường để phục vụ triệu người khác.

### 2. Bảo vệ Tính vẹn toàn của Dữ liệu (Data Integrity)

Giả sử bạn đang làm ứng dụng Chuyển tiền Ngân hàng:

- Bước 1: Trừ tiền tài khoản A.
- Bước 2: Cộng tiền tài khoản B.

Nếu Bước 2 gặp sự cố (mất mạng, đứt cáp), khối `except` sẽ được kích hoạt để thực hiện lệnh **Rollback (Hoàn tiền lại cho A)**. Nếu không có ngoại lệ, tài khoản A sẽ mất tiền mà tài khoản B không nhận được.

### 3. Đảm bảo Tài nguyên luôn được Giải phóng (`finally` / Context Manager)

Dù đoạn code xử lý file hay kết nối Database có bị lỗi nặng đến đâu, khối `finally` (hoặc `with open`) **luôn luôn được gọi** để đóng kết nối. Điều này ngăn chặn triệt để tình trạng rò rỉ RAM (Memory Leak) và kẹt ổ cứng.

---

## 💡 Tóm lại

Ngoại lệ (Exception) **không phải là một "Bug"**, mà là một **Cơ chế báo động an toàn** được tích hợp ở cấp độ Ngôn ngữ và Hệ điều hành.

Nó biến các sự cố không lường trước (ổ cứng đầy, đứt mạng, file hỏng) từ một **"Thảm họa làm sập phần mềm"** trở thành một **"Sự kiện có thể kiểm soát và phục hồi được"**.
