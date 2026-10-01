from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Integer, String, Sequence
class Base(DeclarativeBase):
    pass
class UserORM(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(Integer, Sequence("user_id_seq"), primary_key= True, autoincrement= True)
    name: Mapped[str] = mapped_column(String(100), nullable= False)
    email: Mapped[str] = mapped_column(String(255), unique= True, nullable= False)
    phone_number: Mapped[str] = mapped_column(String(20), nullable= False)
    password: Mapped[str] = mapped_column(String(255), nullable= False)
    role: Mapped[str] = mapped_column(String(50), default= "user", nullable= False)