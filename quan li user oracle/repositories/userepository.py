from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models.user import UserResponse, UserCreate, UserRole
from models.user_entity import UserORM
from core.database import Database
from core.logger import logger

class UserRepository:
    def __init__(self, db: Database | None = None):
        self.db = db if db is not None else Database()
    def map_to_response(self, entity: UserORM):
        return UserResponse(
            user_id= entity.user_id,
            name = entity.name,
            email = entity.email,
            phone_number= entity.phone_number,
            role= entity.role
        )
    def add(self, user: UserCreate, role: UserRole = UserRole.USER):
        user_entity = UserORM(
            name = user.name,
            email = user.email,
            phone_number = user.phone_number,
            password = user.password,
            role = role.value
        )
        try:
            with self.db.get_connection() as conn:
                with Session(bind= conn) as session:
                    session.add(user_entity)
                    session.flush()
                    session.refresh(user_entity)
                    return self.map_to_response(user_entity)
        except IntegrityError as e:
            if "ORA-00001" in str(e.orig):
                logger.warning("trùng email")
                raise ValueError("email đã được sử dụng")
            logger.error(f"lỗi ràng buộc: {str(e)}", exc_info= True)
            raise
    def list_all(self):
        with self.db.get_connection() as conn:
            with Session(bind= conn) as session:
                stmt = select(UserORM)
                users = session.scalars(stmt).all()
                return [self.map_to_response(u) for u in users]
    def find_by_id(self, user_id: int):
        with self.db.get_connection() as conn:
            with Session(bind= conn) as session:
                user = session.get(UserORM, user_id)
                return self.map_to_response(user) if user else None
    def find_by_email(self,email: str):
        with self.db.get_connection() as conn:
            with Session(bind= conn) as session:
                stmt = select(UserORM).where(UserORM.email == email)
                user = session.scalars(stmt).first()
                if not user:
                    return None
                return{
                    "user_id": user.user_id,
                    "name": user.name,
                    "phone_number": user.phone_number,
                    "password": user.password,
                    "role": user.role,
                }# đưa về dạng dict
    def update(self, user_id: int, user: UserResponse, role: str = "user"):
        with self.db.get_connection() as conn:
            with Session(bind=conn) as session:
                existing_user = session.get(UserORM, user_id)
                if not existing_user:
                    return False
                existing_user.name = user.name
                existing_user.email = user.email
                existing_user.phone_number = user.phone_number
                existing_user.password = user.password
                existing_user.role = user.role
                session.flush()
                return True
    def delete(self, user_id: int):
        with self.db.get_connection() as conn:
            with Session(bind= conn) as session:
                user = session.get(UserORM, user_id)
                if not user:
                    return False
                session.delete(user)
                session.flush()
                return True