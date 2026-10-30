import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_current_user
from core.database import get_db
from models.entities import User
from repositories.model_repositories import UserRepositories
from schema.user import UserResponse, UserUpdate
from services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.put("/{user_id}", response_model=UserResponse)
async def update_profile(
    user_id: uuid.UUID,
    user_in: UserUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    user_repo = UserRepositories(session)
    service = UserService(user_repo)
    
    # Chỉ truyền các trường được gửi lên, bỏ qua None
    update_data = user_in.model_dump(exclude_unset=True)
    return await service.update_profile(user_id, current_user, **update_data)