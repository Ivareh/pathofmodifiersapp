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
        condition='"modifier"."maxRoll" >= "modifier"."minRoll"',
    )

    op.create_check_constraint(
        constraint_name="check_modifier_if_minMaxRolls_then_not_textRoll_or_static_vv",
        table_name="modifier",
        condition=""" (("modifier"."minRoll" IS NOT NULL AND "modifier"."maxRoll" IS NOT NULL) AND "modifier"."textRoll" IS NULL)
    OR
    ("modifier"."textRoll" IS NOT NULL AND ("modifier"."minRoll" IS NULL AND "modifier"."maxRoll" IS NULL))""",
    )

    op.create_check_constraint(
        constraint_name="check_modifier_if_or_not_minRoll_then_maxRoll_vv",
        table_name="modifier",
        condition='("modifier"."minRoll" IS NOT NULL AND "modifier"."maxRoll" IS NOT NULL) OR ("modifier"."minRoll" IS NULL AND "modifier"."maxRoll" IS NULL)',
    )

    op.create_check_constraint(
        constraint_name="check_modifier_static_conditions",
        table_name="modifier",
        condition="""("modifier"."static" = TRUE AND "modifier"."textRoll" IS NULL AND ("modifier"."minRoll" IS NULL AND "modifier"."maxRoll" IS NULL)) 
        OR 
        (("modifier"."static" IS NULL OR "modifier"."static" = FALSE) AND 
        (modifier."textRoll" IS NOT NULL OR (modifier."minRoll" IS NOT NULL AND 
        modifier."maxRoll" IS NOT NULL)))""",
    )

    op.create_check_constraint(
        constraint_name="check_modifier_regex_rolls_conditions_and_static",
        table_name="modifier",
        condition="""
     (
        (modifier."textRoll" IS NOT NULL OR (modifier."maxRoll" IS NOT NULL AND modifier."minRoll" IS NOT NULL))
        AND modifier."regex" IS NOT NULL
        AND (modifier."static" IS NULL OR modifier."static" = false)
    )
    OR (
        (modifier."textRoll" IS NULL OR (modifier."maxRoll" IS NULL AND modifier."minRoll" IS NULL))
        AND modifier."regex" IS NOT NULL
        AND modifier."static" = TRUE
    )""",
    )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("check_modifier_static_conditions", "modifier", type_="check")
    op.drop_constraint(
        "check_modifier_if_or_not_minRoll_then_maxRoll_vv", "modifier", type_="check"
    )
    op.drop_constraint(
        "check_modifier_if_minMaxRolls_then_not_textRoll_or_static_vv", "modifier", type_="check"
    )
    op.drop_constraint(
        "check_modifier_maxRoll_greaterThan_minRoll", "modifier", type_="check"
    )
    op.drop_constraint("check_modifier_regex_rolls_conditions_and_static", "modifier", type_="check")
    # ### end Alembic commands ###
