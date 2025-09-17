"""replace shift with shift_type and custom_shift

Revision ID: 53e92650880d
Revises: be7ff54ef605
Create Date: 2025-09-17 12:58:58.002770
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "53e92650880d"
down_revision: Union[str, Sequence[str], None] = "be7ff54ef605"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Define the enum type explicitly
shift_enum = sa.Enum("MORNING", "DAY", "EVENING", "NIGHT", name="shifttype")


def upgrade() -> None:
    # Create the enum type first
    shift_enum.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "schedule_archives", sa.Column("shift_type", shift_enum, nullable=True)
    )
    op.add_column(
        "schedule_archives",
        sa.Column("custom_shift", sa.String(length=50), nullable=True),
    )
    op.drop_column("schedule_archives", "shift")

    op.add_column("schedules", sa.Column("shift_type", shift_enum, nullable=True))
    op.add_column(
        "schedules", sa.Column("custom_shift", sa.String(length=50), nullable=True)
    )
    op.drop_column("schedules", "shift")


def downgrade() -> None:
    op.add_column(
        "schedules",
        sa.Column("shift", sa.VARCHAR(length=20), autoincrement=False, nullable=False),
    )
    op.drop_column("schedules", "custom_shift")
    op.drop_column("schedules", "shift_type")

    op.add_column(
        "schedule_archives",
        sa.Column("shift", sa.VARCHAR(length=20), autoincrement=False, nullable=False),
    )
    op.drop_column("schedule_archives", "custom_shift")
    op.drop_column("schedule_archives", "shift_type")

    # Drop the enum type when rolling back
    shift_enum.drop(op.get_bind(), checkfirst=True)
