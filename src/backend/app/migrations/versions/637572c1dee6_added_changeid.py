"""Added changeId

Revision ID: 637572c1dee6
Revises: 98edf7a48921
Create Date: 2024-03-27 09:41:06.779019

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '637572c1dee6'
down_revision: Union[str, None] = '98edf7a48921'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item', sa.Column('changeId', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('item', 'changeId')
    # ### end Alembic commands ###