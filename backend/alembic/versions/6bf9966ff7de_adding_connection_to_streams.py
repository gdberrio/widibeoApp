"""adding connection to streams

Revision ID: 6bf9966ff7de
Revises: 9530bdd30f15
Create Date: 2023-09-08 09:10:32.326776

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6bf9966ff7de'
down_revision: Union[str, None] = '9530bdd30f15'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
