"""Initial migration

Revision ID: 57bb804925b6
Revises:
Create Date: 2025-05-14 20:14:06.380863

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '57bb804925b6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('groupe_parlementaire',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_groupe_parlementaire_name'), 'groupe_parlementaire', ['name'], unique=False)
    op.create_table('region',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_region_name'), 'region', ['name'], unique=True)
    op.create_table('departement',
    sa.Column('code', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('region_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['region_id'], ['region.id'], ),
    sa.PrimaryKeyConstraint('code')
    )
    op.create_index(op.f('ix_departement_name'), 'departement', ['name'], unique=False)
    op.create_table('circonscription',
    sa.Column('departement_code', sa.String(), nullable=False),
    sa.Column('code', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['departement_code'], ['departement.code'], ),
    sa.PrimaryKeyConstraint('departement_code', 'code')
    )
    op.create_table('depute',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('last_name_normalize', sa.String(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('first_name_normalize', sa.String(), nullable=False),
    sa.Column('gp_id', sa.String(), nullable=False),
    sa.Column('circonscription_departement_code', sa.String(), nullable=False),
    sa.Column('circonscription_code', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['circonscription_departement_code', 'circonscription_code'], ['circonscription.departement_code', 'circonscription.code'], ),
    sa.ForeignKeyConstraint(['gp_id'], ['groupe_parlementaire.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_depute_first_name_normalize'), 'depute', ['first_name_normalize'], unique=False)
    op.create_index(op.f('ix_depute_last_name_normalize'), 'depute', ['last_name_normalize'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_depute_last_name_normalize'), table_name='depute')
    op.drop_index(op.f('ix_depute_first_name_normalize'), table_name='depute')
    op.drop_table('depute')
    op.drop_table('circonscription')
    op.drop_index(op.f('ix_departement_name'), table_name='departement')
    op.drop_table('departement')
    op.drop_index(op.f('ix_region_name'), table_name='region')
    op.drop_table('region')
    op.drop_index(op.f('ix_groupe_parlementaire_name'), table_name='groupe_parlementaire')
    op.drop_table('groupe_parlementaire')
