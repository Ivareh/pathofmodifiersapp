"""Removed unique constraint on category

Revision ID: 3ac53017d0c3
Revises: 8347f3b38e31
Create Date: 2024-03-27 18:05:59.157183

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3ac53017d0c3'
down_revision: Union[str, None] = '8347f3b38e31'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('item_base_type_category_key', 'item_base_type', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('item_base_type_category_key', 'item_base_type', ['category'])
    # ### end Alembic commands ###