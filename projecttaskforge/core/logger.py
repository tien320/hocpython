import logging
import os
from logging.handlers import RotatingFileHandler

# Tạo thư mục logs nếu chưa tồn tại
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Định dạng dòng log: Thời gian - Tên module - Cấp độ lỗi - Thông điệp
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logger(name: str = "app") -> logging.Logger:
    logger = logging.getLogger(name)

    # Tránh gắn lặp handlers nếu hàm bị gọi nhiều lần
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)

    # 1. Handler xuất ra màn hình Terminal (Console)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)

    # 2. Handler ghi ra file xoay vòng (tối đa 10MB/file, lưu tối đa 5 file backup)
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.WARNING)  # Chỉ ghi WARNING & ERROR vào file
    logger.addHandler(file_handler)

    return logger


# Instance dùng chung cho toàn bộ dự án
logger = setup_logger("app")