"""Initial migration - create todos table.

Revision ID: 001
Revises:
Create Date: 2024-01-01 00:00:00

"""
from typing import Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, None] = None
depends_on: Union[str, None] = None


def upgrade() -> None:
    """Create todos table."""
    op.create_table(
        "todos",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_completed", sa.Boolean(), nullable=False, default=False),
        sa.Column("due_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_todos_id"), "todos", ["id"], unique=False)
    op.create_index(op.f("ix_todos_title"), "todos", ["title"], unique=False)
    op.create_index(op.f("ix_todos_is_completed"), "todos", ["is_completed"], unique=False)
    op.create_index(op.f("ix_todos_due_at"), "todos", ["due_at"], unique=False)


def downgrade() -> None:
    """Drop todos table."""
    op.drop_index(op.f("ix_todos_due_at"), table_name="todos")
    op.drop_index(op.f("ix_todos_is_completed"), table_name="todos")
    op.drop_index(op.f("ix_todos_title"), table_name="todos")
    op.drop_index(op.f("ix_todos_id"), table_name="todos")
    op.drop_table("todos")
