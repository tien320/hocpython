"""Baseline for the existing TASKFORGE Oracle schema.

Revision ID: 0001_oracle_schema_baseline
Revises:
Create Date: 2026-10-23
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle


revision: str = "0001_oracle_schema_baseline"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


class _OracleVarchar2Byte(sa.types.UserDefinedType):
    cache_ok = True

    def __init__(self, length: int):
        self.length = length

    def get_col_spec(self, **kw) -> str:
        return f"VARCHAR2({self.length} BYTE)"


class _OracleTimestamp6WithTimeZone(sa.types.UserDefinedType):
    cache_ok = True

    def get_col_spec(self, **kw) -> str:
        return "TIMESTAMP(6) WITH TIME ZONE"


def _timestamp_column(name: str) -> sa.Column:
    return sa.Column(
        name,
        _OracleTimestamp6WithTimeZone(),
        server_default=sa.text("CURRENT_TIMESTAMP"),
        nullable=False,
    )


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column(
            "id",
            oracle.RAW(16),
            server_default=sa.text("SYS_GUID()"),
            nullable=False,
        ),
        sa.Column("email", _OracleVarchar2Byte(255), nullable=False),
        sa.Column("password_hash", _OracleVarchar2Byte(255), nullable=False),
        sa.Column("full_name", _OracleVarchar2Byte(255), nullable=False),
        _timestamp_column("created_at"),
        _timestamp_column("updated_at"),
        sa.PrimaryKeyConstraint("id", name="PK_USERS"),
        sa.UniqueConstraint("email", name="UQ_USERS_EMAIL"),
    )

    op.create_table(
        "workspaces",
        sa.Column(
            "id",
            oracle.RAW(16),
            server_default=sa.text("SYS_GUID()"),
            nullable=False,
        ),
        sa.Column("name", _OracleVarchar2Byte(255), nullable=False),
        sa.Column("slug", _OracleVarchar2Byte(255), nullable=False),
        sa.Column("owner_id", oracle.RAW(16), nullable=False),
        _timestamp_column("created_at"),
        _timestamp_column("updated_at"),
        sa.PrimaryKeyConstraint("id", name="PK_WORKSPACES"),
        sa.UniqueConstraint("slug", name="UQ_WORKSPACES_SLUG"),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["users.id"],
            name="FK_WORKSPACES_OWNER",
            ondelete="CASCADE",
        ),
    )

    op.create_table(
        "projects",
        sa.Column(
            "id",
            oracle.RAW(16),
            server_default=sa.text("SYS_GUID()"),
            nullable=False,
        ),
        sa.Column("workspace_id", oracle.RAW(16), nullable=False),
        sa.Column("name", _OracleVarchar2Byte(255), nullable=False),
        sa.Column("key", _OracleVarchar2Byte(50), nullable=False),
        sa.Column("description", oracle.CLOB(), nullable=True),
        sa.Column("created_by", oracle.RAW(16), nullable=False),
        _timestamp_column("created_at"),
        _timestamp_column("updated_at"),
        sa.PrimaryKeyConstraint("id", name="PK_PROJECTS"),
        sa.UniqueConstraint(
            "workspace_id",
            "key",
            name="UQ_PROJECTS_WS_KEY",
        ),
        sa.ForeignKeyConstraint(
            ["workspace_id"],
            ["workspaces.id"],
            name="FK_PROJECTS_WORKSPACE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["users.id"],
            name="FK_PROJECTS_CREATOR",
            ondelete="CASCADE",
        ),
    )

    op.create_table(
        "tasks",
        sa.Column(
            "id",
            oracle.RAW(16),
            server_default=sa.text("SYS_GUID()"),
            nullable=False,
        ),
        sa.Column("project_id", oracle.RAW(16), nullable=False),
        sa.Column("title", _OracleVarchar2Byte(255), nullable=False),
        sa.Column("description", oracle.CLOB(), nullable=True),
        sa.Column("status", _OracleVarchar2Byte(30), nullable=False),
        sa.Column("priority", _OracleVarchar2Byte(30), nullable=False),
        sa.Column("creator_id", oracle.RAW(16), nullable=False),
        sa.Column("assignee_id", oracle.RAW(16), nullable=True),
        _timestamp_column("created_at"),
        _timestamp_column("updated_at"),
        sa.CheckConstraint(
            "status IN ('TODO', 'IN_PROGRESS', 'IN_REVIEW', 'DONE', 'CANCELLED')",
            name="CHK_TASKS_STATUS",
        ),
        sa.CheckConstraint(
            "priority IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')",
            name="CHK_TASKS_PRIORITY",
        ),
        sa.PrimaryKeyConstraint("id", name="PK_TASKS"),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"],
            name="FK_TASKS_PROJECT",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["creator_id"],
            ["users.id"],
            name="FK_TASKS_CREATOR",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["assignee_id"],
            ["users.id"],
            name="FK_TASKS_ASSIGNEE",
            ondelete="SET NULL",
        ),
    )

    op.create_table(
        "workspace_members",
        sa.Column("workspace_id", oracle.RAW(16), nullable=False),
        sa.Column("user_id", oracle.RAW(16), nullable=False),
        sa.Column("role", _OracleVarchar2Byte(20), nullable=False),
        _timestamp_column("joined_at"),
        sa.CheckConstraint(
            "role IN ('OWNER', 'ADMIN', 'MEMBER')",
            name="CHK_WM_ROLE",
        ),
        sa.PrimaryKeyConstraint(
            "workspace_id",
            "user_id",
            name="PK_WORKSPACE_MEMBERS",
        ),
        sa.ForeignKeyConstraint(
            ["workspace_id"],
            ["workspaces.id"],
            name="FK_WM_WORKSPACE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="FK_WM_USER",
            ondelete="CASCADE",
        ),
    )

    op.create_table(
        "comments",
        sa.Column(
            "id",
            oracle.RAW(16),
            server_default=sa.text("SYS_GUID()"),
            nullable=False,
        ),
        sa.Column("task_id", oracle.RAW(16), nullable=False),
        sa.Column("user_id", oracle.RAW(16), nullable=False),
        sa.Column("content", oracle.CLOB(), nullable=False),
        _timestamp_column("created_at"),
        _timestamp_column("updated_at"),
        sa.PrimaryKeyConstraint("id", name="PK_COMMENTS"),
        sa.ForeignKeyConstraint(
            ["task_id"],
            ["tasks.id"],
            name="FK_COMMENTS_TASK",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="FK_COMMENTS_USER",
            ondelete="CASCADE",
        ),
    )

    op.create_index("IDX_COMMENTS_TASK", "comments", ["task_id"])
    op.create_index("IDX_COMMENTS_USER", "comments", ["user_id"])
    op.create_index("IDX_PROJECTS_WORKSPACE", "projects", ["workspace_id"])
    op.create_index("IDX_PROJECTS_CREATOR", "projects", ["created_by"])
    op.create_index("IDX_TASKS_ASSIGNEE", "tasks", ["assignee_id"])
    op.create_index("IDX_TASKS_PROJECT", "tasks", ["project_id"])
    op.create_index("IDX_TASKS_CREATOR", "tasks", ["creator_id"])
    op.create_index("IDX_WORKSPACES_OWNER", "workspaces", ["owner_id"])


def downgrade() -> None:
    """Drop all six tables and their data; use only when that loss is intended."""
    op.drop_table("comments")
    op.drop_table("workspace_members")
    op.drop_table("tasks")
    op.drop_table("projects")
    op.drop_table("workspaces")
    op.drop_table("users")
