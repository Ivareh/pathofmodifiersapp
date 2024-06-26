"""Removed changeId from item

Revision ID: c88ade998b10
Revises: 1757a2a4be5e
Create Date: 2024-05-22 10:28:47.352196

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c88ade998b10"
down_revision: Union[str, None] = "1757a2a4be5e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("item", "changeId")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "item", sa.Column("changeId", sa.VARCHAR(), autoincrement=False, nullable=False)
    )
    # ### end Alembic commands ###
