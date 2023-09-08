"""small fix to stream

Revision ID: 9530bdd30f15
Revises: 9161497c0530
Create Date: 2023-09-08 08:53:42.268861

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9530bdd30f15'
down_revision: Union[str, None] = '9161497c0530'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('streams', sa.Column('source_id', sa.String(), nullable=True))
    op.add_column('streams', sa.Column('destination_id', sa.String(), nullable=True))
    op.drop_index('ix_streams_name', table_name='streams')
    op.create_foreign_key(None, 'streams', 'destinations', ['destination_id'], ['id'])
    op.create_foreign_key(None, 'streams', 'sources', ['source_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'streams', type_='foreignkey')
    op.drop_constraint(None, 'streams', type_='foreignkey')
    op.create_index('ix_streams_name', 'streams', ['name'], unique=False)
    op.drop_column('streams', 'destination_id')
    op.drop_column('streams', 'source_id')
    # ### end Alembic commands ###
