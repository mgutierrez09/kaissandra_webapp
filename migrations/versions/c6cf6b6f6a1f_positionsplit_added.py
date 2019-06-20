"""positionSplit added

Revision ID: c6cf6b6f6a1f
Revises: a0603b224a85
Create Date: 2019-06-20 17:58:01.130252

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6cf6b6f6a1f'
down_revision = 'a0603b224a85'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('positionsplit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userlots', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('positionsplit')
    # ### end Alembic commands ###