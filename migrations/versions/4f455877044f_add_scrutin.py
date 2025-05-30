"""Add scrutin

Revision ID: 4f455877044f
Revises: 57bb804925b6
Create Date: 2025-05-21 21:01:57.466688

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4f455877044f'
down_revision: Union[str, None] = '57bb804925b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('scrutin',
    sa.Column('id', sa.String(32), nullable=False),
    sa.Column('titre', sa.String(255), nullable=False),
    sa.Column('date_scrutin', sa.Date(), nullable=False),
    sa.Column('sort', sa.String(32), nullable=False),
    sa.Column('type', sa.String(32), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vote',
    sa.Column('scrutin_id', sa.String(32), nullable=False),
    sa.Column('depute_id', sa.String(32), nullable=False),
    sa.Column('ballot', sa.Enum('ABSENT', 'NONVOTANT', 'POUR', 'CONTRE', 'ABSTENTION', name='ballot'), nullable=False),
    sa.ForeignKeyConstraint(['depute_id'], ['depute.id'], ),
    sa.ForeignKeyConstraint(['scrutin_id'], ['scrutin.id'], ),
    sa.PrimaryKeyConstraint('scrutin_id', 'depute_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vote')
    op.drop_table('scrutin')
    # ### end Alembic commands ###
