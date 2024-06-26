"""Create constraints for textrolls, modifier.maxRoll, modifier.minRoll

Revision ID: ee098521790e
Revises: 8e367f7f8609
Create Date: 2024-02-21 20:24:32.761582

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import validates


# revision identifiers, used by Alembic.
revision: str = "ee098521790e"
down_revision: Union[str, None] = "8e367f7f8609"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_check_constraint(
        constraint_name="check_modifier_maxRoll_greaterThan_minRoll",
        table_name="modifier",
        condition=""" modifier."maxRoll" > modifier."minRoll" """,
    )
    op.create_check_constraint(
        constraint_name="check_modifier_if_static_else_check_rolls_and_regex",
        table_name="modifier",
        condition="""
                    CASE 
                        WHEN (modifier.static = TRUE) 
                        THEN (
                                (modifier."minRoll" IS NULL AND modifier."maxRoll" IS NULL)
                                AND modifier."textRolls" IS NULL 
                                AND modifier.regex IS NULL
                            )
                        ELSE (
                                (
                                    (
                                        (modifier."minRoll" IS NOT NULL AND modifier."maxRoll" IS NOT NULL)
                                        AND modifier."textRolls" IS NULL
                                    )
                                    OR
                                    (
                                        (modifier."minRoll" IS  NULL AND modifier."maxRoll" IS  NULL)
                                        AND modifier."textRolls" IS NOT NULL
                                    )
                                )
                                AND modifier.regex IS NOT NULL
                            )
                    END
                    """,
    )
    op.create_check_constraint(
        constraint_name="check_modifier_if_not_static_then_modifier_contains_hashtag",
        table_name="modifier",
        condition="""
                    CASE
                        WHEN modifier.static = TRUE
                        THEN (
                            modifier.effect NOT LIKE '%#%'
                            )
                        ELSE (
                            modifier.effect LIKE '%#%'
                        )
                    END
                    """,
    )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "check_modifier_maxRoll_greaterThan_minRoll", "modifier", type_="check"
    )
    op.drop_constraint(
        "check_modifier_if_static_else_check_rolls_and_regex", "modifier", type_="check"
    )
    op.drop_constraint(
        "check_modifier_if_static_then_modifier_contains_pound",
        "modifier",
        type_="check",
    )
