"""change monetary columns from float to integer cents

Revision ID: 6f34c3b077d7
Revises: 05ac6bd215e8
Create Date: 2026-02-05 17:53:06.293400

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6f34c3b077d7"
down_revision: Union[str, Sequence[str], None] = "05ac6bd215e8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("budgets") as batch_op:
        batch_op.alter_column(
            "amount_limit",
            existing_type=sa.FLOAT(),
            type_=sa.Integer(),
            existing_nullable=False,
        )
    with op.batch_alter_table("recurrence_groups") as batch_op:
        batch_op.alter_column(
            "expected_amount",
            existing_type=sa.FLOAT(),
            type_=sa.Integer(),
            existing_nullable=False,
        )
    with op.batch_alter_table("transactions") as batch_op:
        batch_op.alter_column(
            "amount",
            existing_type=sa.FLOAT(),
            type_=sa.Integer(),
            existing_nullable=False,
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("transactions") as batch_op:
        batch_op.alter_column(
            "amount",
            existing_type=sa.Integer(),
            type_=sa.FLOAT(),
            existing_nullable=False,
        )
    with op.batch_alter_table("recurrence_groups") as batch_op:
        batch_op.alter_column(
            "expected_amount",
            existing_type=sa.Integer(),
            type_=sa.FLOAT(),
            existing_nullable=False,
        )
    with op.batch_alter_table("budgets") as batch_op:
        batch_op.alter_column(
            "amount_limit",
            existing_type=sa.Integer(),
            type_=sa.FLOAT(),
            existing_nullable=False,
        )
