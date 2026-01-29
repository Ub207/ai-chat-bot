"""Add missing priority and user_id columns to todos table.

Revision ID: 002
Revises: 001
Create Date: 2026-01-28 10:00:00

"""
from typing import Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, None] = None
depends_on: Union[str, None] = None


def upgrade() -> None:
    """Add priority and user_id columns to todos table."""
    # Add priority column with default value
    op.add_column('todos', sa.Column('priority', sa.Integer(), nullable=False, default=0))

    # Add user_id column with default value (assuming user_id=1 for existing records)
    op.add_column('todos', sa.Column('user_id', sa.Integer(), nullable=False, default=1))

    # Create index for user_id
    op.create_index(op.f('ix_todos_user_id'), 'todos', ['user_id'], unique=False)

    # Update existing records to have user_id = 1
    op.execute("UPDATE todos SET user_id = 1 WHERE user_id IS NULL OR user_id = ''")

    # Update existing records to have priority = 0
    op.execute("UPDATE todos SET priority = 0 WHERE priority IS NULL")


def downgrade() -> None:
    """Remove priority and user_id columns from todos table."""
    op.drop_index(op.f('ix_todos_user_id'), table_name='todos')
    op.drop_column('todos', 'user_id')
    op.drop_column('todos', 'priority')