import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_current_user
from core.database import get_db
from models.entities import User
from repositories.model_repositories import ProjectRepository, WorkspaceMemberRepository
from schema.project import ProjectCreate, ProjectResponse, ProjectUpdate

router = APIRouter(tags=["Projects"])


@router.post("/workspaces/{workspace_id}/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    workspace_id: uuid.UUID,
    data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    member_repo = WorkspaceMemberRepository(session)
    member = await member_repo.get_member(workspace_id, current_user.id)
    if not member:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không thuộc workspace này")

    project_repo = ProjectRepository(session)
    # Kiểm tra key dự án trùng trong workspace
    existing = await project_repo.get_by_workspace_and_key(workspace_id, data.key)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mã Key dự án đã tồn tại trong workspace")

    return await project_repo.create(
        workspace_id=workspace_id,
        name=data.name,
        key=data.key,
        description=data.description,
        created_by_id=current_user.id,
    )


@router.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    project_repo = ProjectRepository(session)
    project = await project_repo.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy dự án")

    member_repo = WorkspaceMemberRepository(session)
    member = await member_repo.get_member(project.workspace_id, current_user.id)
    if not member:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không có quyền truy cập dự án này")

    return project


@router.put("/projects/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: uuid.UUID,
    data: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    project_repo = ProjectRepository(session)
    project = await project_repo.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy dự án")

    update_data = data.model_dump(exclude_unset=True)
    return await project_repo.update(project_id, **update_data)


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    project_repo = ProjectRepository(session)
    project = await project_repo.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy dự án")

    await project_repo.delete(project_id)