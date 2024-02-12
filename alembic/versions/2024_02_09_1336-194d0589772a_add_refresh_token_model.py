"""add refresh token model

Revision ID: 194d0589772a
Revises: a9e84db2ff22
Create Date: 2024-02-09 13:36:17.525968

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '194d0589772a'
down_revision: Union[str, None] = 'a9e84db2ff22'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('refresh_token',
    sa.Column('refresh_token_id', sa.Integer(), nullable=False),
    sa.Column('refresh_key', sa.Uuid(), nullable=False),
    sa.Column('exp', sa.DateTime(timezone=True), nullable=False),
    sa.Column('iat', sa.DateTime(timezone=True), nullable=False),
    sa.Column('access_key', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('refresh_token_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('refresh_token')
    # ### end Alembic commands ###