import uuid
from fastapi import HTTPException, status
from models.enums import WorkspaceRole
from repositories.model_repositories import WorkspaceMemberRepository


class WorkspaceService:
    def __init__(self, member_repo: WorkspaceMemberRepository):
        self.member_repo = member_repo

    async def ensure_is_admin_or_owner(self, workspace_id: uuid.UUID, user_id: uuid.UUID):
        membership = await self.member_repo.get_member(workspace_id, user_id)
        if not membership or membership.role not in [WorkspaceRole.ADMIN, WorkspaceRole.OWNER]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Chỉ OWNER hoặc ADMIN mới được thực hiện thao tác này",
            )
        return membership

    async def remove_member_from_workspace(
        self, workspace_id: uuid.UUID, target_user_id: uuid.UUID, actor_user_id: uuid.UUID
    ):
        actor_membership = await self.ensure_is_admin_or_owner(workspace_id, actor_user_id)
        
        target_membership = await self.member_repo.get_member(workspace_id, target_user_id)
        if not target_membership:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thành viên không tồn tại trong workspace")

        # Ràng buộc: Không được xóa OWNER
        if target_membership.role == WorkspaceRole.OWNER:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Không thể xóa OWNER khỏi workspace")

        # Ràng buộc: ADMIN không được xóa ADMIN khác (chỉ OWNER mới có quyền)
        if target_membership.role == WorkspaceRole.ADMIN and actor_membership.role != WorkspaceRole.OWNER:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Chỉ OWNER mới có quyền xóa ADMIN")

        return await self.member_repo.remove_member(workspace_id, target_user_id)