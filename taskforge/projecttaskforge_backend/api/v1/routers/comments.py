import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_current_user
from core.database import get_db
from models.entities import User
from models.enums import WorkspaceRole
from repositories.model_repositories import (
    CommentRepository,
    ProjectRepository,
    TaskRepository,
    WorkspaceMemberRepository,
)
from schema.comment import CommentCreate, CommentResponse, CommentUpdate

router = APIRouter(tags=["Comments"])

async def check_project_access(project_id: uuid.UUID, user_id: uuid.UUID, session: AsyncSession) -> bool:
    project_repo = ProjectRepository(session)
    project = await project_repo.get_by_id(project_id)
    if not project:
        return False

    member_repo = WorkspaceMemberRepository(session)
    return await member_repo.get_member(project.workspace_id, user_id) is not None

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

    # Kiểm tra quyền qua project_id của task
    has_access = await check_project_access(task.project_id, current_user.id, session)
    if not has_access:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không có quyền truy cập task này")

    comment_repo = CommentRepository(session)
    new_comment = await comment_repo.create(
        task_id=task_id,
        user_id=current_user.id,
        content=data.content.strip(),
    )
    new_comment.author = current_user
    return new_comment

@router.get("/tasks/{task_id}/comments", response_model=List[CommentResponse])
async def list_comments_by_task(
    task_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    task_repo = TaskRepository(session)
    task = await task_repo.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy task")

    has_access = await check_project_access(task.project_id, current_user.id, session)
    if not has_access:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không có quyền truy cập task này")

    comment_repo = CommentRepository(session)
    return await comment_repo.get_comments_by_task(task_id)

@router.patch("/comments/{comment_id}", response_model=CommentResponse)
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

    # 1. Kiểm tra chính chủ
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Chỉ tác giả mới được sửa bình luận này")

    # 2. Kiểm tra tác giả có còn thuộc project chứa task đó không
    task_repo = TaskRepository(session)
    task = await task_repo.get_by_id(comment.task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task không còn tồn tại")

    has_access = await check_project_access(task.project_id, current_user.id, session)
    if not has_access:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không còn quyền trong dự án này")

    # 3. Cập nhật
    updated = await comment_repo.update(comment_id, content=data.content.strip())
    updated.author = current_user
    return updated

@router.delete(
    "/comments/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Xóa bình luận"
)
async def delete_comment(
    comment_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    comment_repo = CommentRepository(session)
    comment = await comment_repo.get_by_id(comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Không tìm thấy bình luận"
        )

    # 1. Lấy thông tin Task để xác định Project / Workspace
    task_repo = TaskRepository(session)
    task = await task_repo.get_by_id(comment.task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Task liên kết không tồn tại"
        )

    # 2. Kiểm tra quyền của người gọi API trong Project/Workspace
    has_access = await check_project_access(task.project_id, current_user.id, session)
    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Bạn không có quyền trong dự án này"
        )

    # 3. Phân quyền xóa: Là tác giả HOẶC có vai trò Admin / Project Owner
    is_author = (comment.user_id == current_user.id)
    # Giả sử hàm helper hoặc trường current_user/role check được quyền admin
    project_repo = ProjectRepository(session)
    project = await project_repo.get_by_id(task.project_id)
    member_repo = WorkspaceMemberRepository(session)
    member = await member_repo.get_member(project.workspace_id, current_user.id) if project else None
    is_admin = member is not None and member.role in [WorkspaceRole.ADMIN, WorkspaceRole.OWNER]

    if not (is_author or is_admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Bạn không có quyền xóa bình luận này"
        )

    # 4. Thực hiện xóa (Hard delete qua BaseRepository hoặc Soft delete)
    await comment_repo.delete(comment_id)

    # HTTP 204 No Content không kèm body
    return Response(status_code=status.HTTP_204_NO_CONTENT)