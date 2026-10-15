import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_current_user
from core.database import get_db
from models.entities import User
from repositories.model_repositories import ProjectRepository, TaskRepository
from schema.task import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter(tags=["Tasks"])


@router.post("/projects/{project_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    project_id: uuid.UUID,
    data: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    project_repo = ProjectRepository(session)
    project = await project_repo.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy dự án")

    task_repo = TaskRepository(session)
    task_data = data.model_dump()
    return await task_repo.create(
        project_id=project_id,
        creator_id=current_user.id,
        **task_data,
    )


@router.get("/projects/{project_id}/tasks", response_model=List[TaskResponse])
async def list_tasks_by_project(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    task_repo = TaskRepository(session)
    return await task_repo.get_tasks_by_project(project_id)


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    task_repo = TaskRepository(session)
    task = await task_repo.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy task")
    return task


@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: uuid.UUID,
    data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    task_repo = TaskRepository(session)
    task = await task_repo.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy task")

    update_data = data.model_dump(exclude_unset=True)
    return await task_repo.update(task_id, **update_data)


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    task_repo = TaskRepository(session)
    task = await task_repo.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy task")

    await task_repo.delete(task_id)