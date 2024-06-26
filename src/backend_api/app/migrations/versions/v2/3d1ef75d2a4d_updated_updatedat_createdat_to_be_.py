"""Updated updatedAt, createdAt to be nullable=false, server_default=_dt.datetime.now(_dt.timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f%z')

Revision ID: 3d1ef75d2a4d
Revises: 58e1fc9de124
Create Date: 2024-02-21 14:00:31.666084

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import datetime as _dt

# revision identifiers, used by Alembic.
revision: str = "3d1ef75d2a4d"
down_revision: Union[str, None] = "58e1fc9de124"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "account",
        "createdAt",
        existing_type=postgresql.TIMESTAMP(),
        nullable=False,
        server_default=_dt.datetime.now(_dt.timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S.%f%z"
        ),
    )
    op.alter_column(
        "account",
        "updatedAt",
        existing_type=postgresql.TIMESTAMP(),
        nullable=False,
        server_default=_dt.datetime.now(_dt.timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S.%f%z"
        ),
    )
    op.alter_column(
        "currency",
        "createdAt",
        existing_type=postgresql.TIMESTAMP(),
        nullable=False,
        server_default=_dt.datetime.now(_dt.timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S.%f%z"
        ),
    )
    op.alter_column(
        "item",
        "createdAt",
        existing_type=postgresql.TIMESTAMP(),
        nullable=False,
        server_default=_dt.datetime.now(_dt.timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S.%f%z"
        ),
    )
    op.alter_column(
        "item_base_type",
        "createdAt",
        existing_type=postgresql.TIMESTAMP(),
        nullable=False,
        server_default=_dt.datetime.now(_dt.timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S.%f%z"
        ),
    )
    op.alter_column(
        "item_base_type",
        "updatedAt",
        existing_type=postgresql.TIMESTAMP(),
        nullable=False,
        server_default=_dt.datetime.now(_dt.timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S.%f%z"
        ),
    )
    op.alter_column(
        "modifier",
        "createdAt",
        existing_type=postgresql.TIMESTAMP(),
        server_default=_dt.datetime.now(_dt.timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S.%f%z"
        ),
        nullable=False,
    )
    op.alter_column(
        "modifier",
        "updatedAt",
        existing_type=postgresql.TIMESTAMP(),
        nullable=False,
        server_default=_dt.datetime.now(_dt.timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S.%f%z"
        ),
    )
    op.alter_column(
        "stash",
        "createdAt",
        existing_type=postgresql.TIMESTAMP(),
        nullable=False,
        server_default=_dt.datetime.now(_dt.timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S.%f%z"
        ),
    )
    op.alter_column(
        "stash",
        "updatedAt",
        existing_type=postgresql.TIMESTAMP(),
        nullable=False,
        server_default=_dt.datetime.now(_dt.timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S.%f%z"
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "stash", "updatedAt", existing_type=postgresql.TIMESTAMP(), nullable=True
    )
    op.alter_column(
        "stash", "createdAt", existing_type=postgresql.TIMESTAMP(), nullable=True
    )
    op.alter_column(
        "modifier", "updatedAt", existing_type=postgresql.TIMESTAMP(), nullable=True
    )
    op.alter_column(
        "modifier", "createdAt", existing_type=postgresql.TIMESTAMP(), nullable=True
    )
    op.alter_column(
        "item_base_type",
        "updatedAt",
        existing_type=postgresql.TIMESTAMP(),
        nullable=True,
    )
    op.alter_column(
        "item_base_type",
        "createdAt",
        existing_type=postgresql.TIMESTAMP(),
        nullable=True,
    )
    op.alter_column(
        "item", "createdAt", existing_type=postgresql.TIMESTAMP(), nullable=True
    )
    op.alter_column(
        "currency", "createdAt", existing_type=postgresql.TIMESTAMP(), nullable=True
    )
    op.alter_column(
        "account", "updatedAt", existing_type=postgresql.TIMESTAMP(), nullable=True
    )
    op.alter_column(
        "account", "createdAt", existing_type=postgresql.TIMESTAMP(), nullable=True
    )
    # ### end Alembic commands ###
