import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_current_user
from core.database import get_db
from models.entities import User
from repositories.model_repositories import CommentRepository, TaskRepository
from schema.comment import CommentCreate, CommentResponse, CommentUpdate

router = APIRouter(tags=["Comments"])


@router.post("/tasks/{task_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def add_comment(
    task_id: uuid.UUID,
    data: CommentCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    task_repo = TaskRepository(session)
    task = await task_repo.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy task")

    comment_repo = CommentRepository(session)
    return await comment_repo.create(
        task_id=task_id,
        user_id=current_user.id,
        content=data.content,
    )


@router.get("/tasks/{task_id}/comments", response_model=List[CommentResponse])
async def list_comments_by_task(
    task_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    comment_repo = CommentRepository(session)
    return await comment_repo.get_comments_by_task(task_id)


@router.put("/comments/{comment_id}", response_model=CommentResponse)
async def update_comment(
    comment_id: uuid.UUID,
    data: CommentUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    comment_repo = CommentRepository(session)
    comment = await comment_repo.get_by_id(comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy bình luận")

    # Chỉ tác giả bình luận mới có quyền sửa
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Chỉ tác giả mới được sửa bình luận này")

    return await comment_repo.update(comment_id, content=data.content)


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    comment_repo = CommentRepository(session)
    comment = await comment_repo.get_by_id(comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy bình luận")

    # Chỉ tác giả mới có quyền xóa
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Chỉ tác giả mới được xóa bình luận này")

    await comment_repo.delete(comment_id)