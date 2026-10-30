import uuid
from fastapi import HTTPException, status
from models.entities import User
from repositories.model_repositories import UserRepositories


class UserService:
    def __init__(self, user_repo: UserRepositories):
        self.user_repo = user_repo

    async def update_profile(self, user_id: uuid.UUID, current_user: User, **update_data):
        if current_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Chỉ có thể sửa thông tin của chính mình",
            )
        return await self.user_repo.update(user_id, **update_data)