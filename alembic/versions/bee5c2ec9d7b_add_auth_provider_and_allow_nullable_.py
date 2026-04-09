"""add auth_provider and allow nullable password

Revision ID: bee5c2ec9d7b
Revises: 7f2c0186c829
Create Date: 2026-03-01 18:13:44.233969

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'bee5c2ec9d7b'
down_revision: Union[str, None] = '7f2c0186c829'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    auth_provider_enum = postgresql.ENUM(
        "GOOGLE",
        "LOCAL",
        name="auth_provider",
        create_type=False,
    )
    auth_provider_enum.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "users",
        sa.Column(
            "auth_provider",
            auth_provider_enum,
            nullable=False,
            server_default="LOCAL",
        ),
    )
    op.alter_column(
        "users",
        "password_hash",
        existing_type=sa.VARCHAR(length=255),
        nullable=True,
    )
    op.alter_column(
        "users",
        "auth_provider",
        server_default=None,
    )


def downgrade() -> None:
    op.alter_column(
        "users",
        "password_hash",
        existing_type=sa.VARCHAR(length=255),
        nullable=False,
    )
    op.drop_column("users", "auth_provider")

    auth_provider_enum = postgresql.ENUM(
        "GOOGLE",
        "LOCAL",
        name="auth_provider",
        create_type=False,
    )
    auth_provider_enum.drop(op.get_bind(), checkfirst=True)

