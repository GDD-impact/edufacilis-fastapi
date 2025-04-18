"""Initial migration

Revision ID: d66c34bb0eb3
Revises: 56ac2f0b7734
Create Date: 2025-04-01 08:25:57.635356

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd66c34bb0eb3'
down_revision: Union[str, None] = '56ac2f0b7734'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('login_provider', sa.String(), nullable=True))
    op.add_column('users', sa.Column('profile_completed', sa.Boolean(), nullable=True))
    op.alter_column('users', 'password_hash',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'password_hash',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_column('users', 'profile_completed')
    op.drop_column('users', 'login_provider')
    # ### end Alembic commands ###
