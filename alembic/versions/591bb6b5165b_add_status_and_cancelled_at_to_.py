"""add_status_and_cancelled_at_to_appointments

Revision ID: 591bb6b5165b
Revises: da9ba533e40d
Create Date: 2025-12-27 17:10:54.817823

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "591bb6b5165b"
down_revision: Union[str, None] = "da9ba533e40d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Criar o tipo ENUM primeiro usando SQL direto
    # Os valores devem corresponder ao enum Python (minúsculas)
    op.execute(
        """
        DO $$ BEGIN
            CREATE TYPE appointment_status AS ENUM ('pending', 'confirmed', 'cancelled', 'completed');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """
    )

    # Adicionar as colunas
    op.add_column(
        "appointments",
        sa.Column(
            "status",
            sa.Enum(
                "pending",
                "confirmed",
                "cancelled",
                "completed",
                name="appointment_status",
            ),
            nullable=False,
            server_default="pending",
        ),
    )
    op.add_column(
        "appointments",
        sa.Column("cancelled_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    # Remover as colunas primeiro
    op.drop_column("appointments", "cancelled_at")
    op.drop_column("appointments", "status")

    # Remover o tipo ENUM
    op.execute("DROP TYPE IF EXISTS appointment_status")
