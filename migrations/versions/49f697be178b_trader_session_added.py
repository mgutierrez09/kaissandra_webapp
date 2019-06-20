"""trader-session added

Revision ID: 49f697be178b
Revises: cf2bac4e4b23
Create Date: 2019-06-20 17:51:58.227036

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49f697be178b'
down_revision = 'cf2bac4e4b23'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('session', sa.Column('trader_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'session', 'trader', ['trader_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'session', type_='foreignkey')
    op.drop_column('session', 'trader_id')
    # ### end Alembic commands ###
