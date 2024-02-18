"""cascade delete tokens

Revision ID: 63ff941b810c
Revises: d53175421535
Create Date: 2024-02-18 13:43:33.665544

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '63ff941b810c'
down_revision: Union[str, None] = 'd53175421535'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('refresh_token_user_id_fkey', 'refresh_token', type_='foreignkey')
    op.create_foreign_key(None, 'refresh_token', 'user', ['user_id'], ['user_id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'refresh_token', type_='foreignkey')
    op.create_foreign_key('refresh_token_user_id_fkey', 'refresh_token', 'user', ['user_id'], ['user_id'])
    # ### end Alembic commands ###
