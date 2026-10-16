import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from api.deps import get_current_user
from core.database import get_db
from models.entities import User
from models.enums import WorkspaceRole
from repositories.model_repositories import WorkspaceMemberRepository, WorkspaceRepositories
from schema.workspace import (
    WorkspaceCreate,
    WorkspaceMemberAdd,
    WorkspaceMemberResponse,
    WorkspaceMemberUpdateRole,
    WorkspaceResponse,
    WorkspaceUpdate,
)
from services.workspace_service import WorkspaceService

router = APIRouter(prefix="/workspaces", tags=["Workspaces"])


@router.post("", response_model=WorkspaceResponse, status_code=status.HTTP_201_CREATED)
async def create_workspace(
    data: WorkspaceCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    ws_repo = WorkspaceRepositories(session)
    member_repo = WorkspaceMemberRepository(session)

    # 1. Kiểm tra nhanh slug đã tồn tại chưa
    existing = await ws_repo.get_by_slug(data.slug)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Slug workspace đã tồn tại"
        )

    try:
        # 2. Đóng gói trong một Transaction duy nhất
        async with session.begin():
            workspace = await ws_repo.create(
                name=data.name,
                slug=data.slug,
                owner_id=current_user.id,
            )

            await member_repo.add_member(
                workspace_id=workspace.id,
                user_id=current_user.id,
                role=WorkspaceRole.OWNER,
            )
            
            # Lưu ý: Nếu trong ws_repo.create() hoặc add_member() bạn có gọi session.commit(),
            # hãy BỎ commit bên trong repo đi, để commit ngoài router/unit-of-work quản lý.

        # 3. Refresh lại workspace nếu cần nạp đầy đủ relationship/id trước khi serialize ra response_model
        await session.refresh(workspace)
        return workspace

    except IntegrityError:
        # Bắt trường hợp race-condition bị trùng slug ở tầng DB
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Slug workspace đã tồn tại"
        )


@router.get("/{workspace_id}", response_model=WorkspaceResponse)
async def get_workspace(
    workspace_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    ws_repo = WorkspaceRepositories(session)
    member_repo = WorkspaceMemberRepository(session)

    # Chỉ thành viên của workspace mới được xem thông tin
    member = await member_repo.get_member(workspace_id, current_user.id)
    if not member:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không thuộc workspace này")

    workspace = await ws_repo.get_by_id(workspace_id)
    if not workspace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy workspace")
    return workspace


@router.put("/{workspace_id}", response_model=WorkspaceResponse)
async def update_workspace(
    workspace_id: uuid.UUID,
    data: WorkspaceUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    member_repo = WorkspaceMemberRepository(session)
    service = WorkspaceService(member_repo)
    # Chỉ ADMIN hoặc OWNER mới được sửa thông tin workspace
    await service.ensure_is_admin_or_owner(workspace_id, current_user.id)

    ws_repo = WorkspaceRepositories(session)
    update_data = data.model_dump(exclude_unset=True)
    updated_ws = await ws_repo.update(workspace_id, **update_data)
    return updated_ws


@router.delete("/{workspace_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workspace(
    workspace_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    ws_repo = WorkspaceRepositories(session)
    workspace = await ws_repo.get_by_id(workspace_id)
    if not workspace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy workspace")

    # Chỉ duy nhất OWNER mới được phép xóa toàn bộ workspace
    if workspace.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Chỉ OWNER mới có quyền xóa workspace")

    await ws_repo.delete(workspace_id)


# --- Endpoints Quản lý Thành viên Workspace ---

@router.get("/{workspace_id}/members", response_model=List[WorkspaceMemberResponse])
async def list_workspace_members(
    workspace_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    member_repo = WorkspaceMemberRepository(session)
    member = await member_repo.get_member(workspace_id, current_user.id)
    if not member:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không thuộc workspace này")

    return await member_repo.list_by_workspace(workspace_id)


@router.post("/{workspace_id}/members", response_model=WorkspaceMemberResponse, status_code=status.HTTP_201_CREATED)
async def add_workspace_member(
    workspace_id: uuid.UUID,
    data: WorkspaceMemberAdd,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    member_repo = WorkspaceMemberRepository(session)
    service = WorkspaceService(member_repo)
    await service.ensure_is_admin_or_owner(workspace_id, current_user.id)

    # Kiểm tra thành viên đã tồn tại chưa
    existing = await member_repo.get_member(workspace_id, data.user_id)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Người dùng đã là thành viên")

    return await member_repo.add_member(workspace_id, data.user_id, data.role)


@router.delete("/{workspace_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_workspace_member(
    workspace_id: uuid.UUID,
    user_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    member_repo = WorkspaceMemberRepository(session)
    service = WorkspaceService(member_repo)
    # Tự động validate không xóa Owner, Admin không xóa Admin
    await service.remove_member_from_workspace(workspace_id, target_user_id=user_id, actor_user_id=current_user.id)