import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from api.deps import get_current_user
from core.database import get_db
from models.entities import User
from repositories.model_repositories import ProjectRepository, WorkspaceMemberRepository
from schema.project import ProjectCreate, ProjectResponse, ProjectUpdate
from schema.workspace import WorkspaceRole
router = APIRouter(tags=["Projects"])


@router.post(
    "/workspaces/{workspace_id}/projects",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Tạo dự án mới trong Workspace",
)
async def create_project(
    workspace_id: uuid.UUID,
    data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    # 1. Kiểm tra user có thuộc workspace hay không
    member_repo = WorkspaceMemberRepository(session)
    member = await member_repo.get_member(workspace_id, current_user.id)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không thuộc workspace này",
        )

    if member.role not in [WorkspaceRole.OWNER, WorkspaceRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ quản trị viên mới có quyền tạo dự án",
        )

    project_repo = ProjectRepository(session)
    clean_key = data.key.strip().upper()

    # 2. Tạo dự án và bắt xung đột (Conflict)
    try:
        new_project = await project_repo.create(
            workspace_id=workspace_id,
            name=data.name.strip(),
            key=clean_key,
            description=data.description,
            created_by_id=current_user.id,
        )
        await session.commit()
        return new_project

    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Mã Key dự án đã tồn tại trong workspace này",
        )


@router.patch(
    "/projects/{project_id}",
    response_model=ProjectResponse,
    status_code=status.HTTP_200_OK,
    summary="Cập nhật thông tin dự án",
)
async def update_project(
    project_id: uuid.UUID,
    data: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    project_repo = ProjectRepository(session)
    project = await project_repo.get_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy dự án",
        )

    # 1. Kiểm tra thành viên Workspace
    member_repo = WorkspaceMemberRepository(session)
    member = await member_repo.get_member(project.workspace_id, current_user.id)
    if not member:
        # Giả lập 404 để không rò rỉ ID project
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy dự án",
        )

    # 2. Phân quyền: Chỉ cho phép Project Creator HOẶC Workspace Owner/Admin
    is_creator = project.created_by_id == current_user.id
    is_admin_or_owner = member.role in [WorkspaceRole.OWNER, WorkspaceRole.ADMIN]

    if not (is_creator or is_admin_or_owner):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền chỉnh sửa dự án này",
        )

    # 3. Lấy dữ liệu cần update
    update_data = data.model_dump(exclude_unset=True)
    if not update_data:
        return project

    # Chuẩn hóa nếu có cập nhật key
    if "key" in update_data and update_data["key"]:
        update_data["key"] = update_data["key"].strip().upper()

    # 4. Thực thi cập nhật & bắt lỗi IntegrityError nếu trùng lặp key
    try:
        updated_project = await project_repo.update(project_id, **update_data)
        await session.commit()
        return updated_project

    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Mã Key dự án đã tồn tại trong workspace này",
        )

@router.get(
    "/projects/{project_id}",
    response_model=ProjectResponse,
    status_code=status.HTTP_200_OK,
    summary="Lấy thông tin chi tiết dự án",
)
async def get_project(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    # 1. Tìm dự án
    project_repo = ProjectRepository(session)
    project = await project_repo.get_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy dự án",
        )

    # 2. Kiểm tra quyền truy cập (user phải thuộc workspace chứa project)
    member_repo = WorkspaceMemberRepository(session)
    member = await member_repo.get_member(project.workspace_id, current_user.id)
    if not member:
        # Giả lập 404 để chống dò quét ID dự án của workspace khác
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy dự án",
        )

    return project

@router.delete(
    "/projects/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Xóa dự án",
)
async def delete_project(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    # 1. Tìm project
    project_repo = ProjectRepository(session)
    project = await project_repo.get_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy dự án",
        )

    # 2. Kiểm tra thành viên thuộc workspace chứa project
    member_repo = WorkspaceMemberRepository(session)
    member = await member_repo.get_member(project.workspace_id, current_user.id)
    if not member:
        # Trả về 404 để chống rò rỉ ID project
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy dự án",
        )

    # 3. Phân quyền: Chỉ Workspace Owner hoặc Admin mới có quyền xóa
    if member.role not in [WorkspaceRole.OWNER, WorkspaceRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ quản trị viên hoặc chủ sở hữu workspace mới có quyền xóa dự án",
        )

    # 4. Thực thi xóa và commit
    await project_repo.delete(project_id)
    await session.commit()

    # Với 204 No Content, trả về Response rỗng
    return Response(status_code=status.HTTP_204_NO_CONTENT)