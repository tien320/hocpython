import sys
from os.path import abspath, dirname
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import URL
from alembic import context

# 1. Thêm đường dẫn thư mục gốc của project vào sys.path để tránh lỗi ModuleNotFoundError
sys.path.insert(0, dirname(dirname(abspath(__file__))))

from core.config import settings
from models.user_entity import Base

# Alembic Config object
config = context.config

# Cấu hình logging của Alembic
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 2. Gán Metadata của ORM để Alembic nhận diện bảng users
target_metadata = Base.metadata

# 3. Chuyển đổi DSN (localhost:1521/XEPDB1) thành SQLAlchemy URL chuẩn cho Oracle Service Name
# Dạng URL sinh ra: oracle+oracledb://usermanage:123456@localhost:1521/?service_name=XEPDB1
try:
    host_port, service_name = settings.DB_DSN.split("/")
    host, port = host_port.split(":")
    port = int(port)
except Exception:
    # Giá trị dự phòng nếu DSN có định dạng khác
    host = "localhost"
    port = 1521
    service_name = "XEPDB1"

oracle_url = URL.create(
    drivername="oracle+oracledb",
    username=settings.DB_USER.strip(),
    password=settings.DB_PASSWORD.strip(),
    host=host.strip(),
    port=port,
    query={"service_name": service_name.strip()},
)

# Nạp URL vào config của Alembic
config.set_main_option(
    "sqlalchemy.url", 
    oracle_url.render_as_string(hide_password=False)
)


def run_migrations_offline() -> None:
    """Chạy migration ở chế độ offline (sinh mã SQL thuần)"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Chạy migration trực tiếp vào Oracle Database"""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # Theo dõi cả sự thay đổi kiểu dữ liệu cột
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()