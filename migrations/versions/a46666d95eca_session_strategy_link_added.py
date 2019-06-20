"""session-strategy link added

Revision ID: a46666d95eca
Revises: 49f697be178b
Create Date: 2019-06-20 17:52:47.711495

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a46666d95eca'
down_revision = '49f697be178b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sessionstratetgy',
    sa.Column('session_id', sa.Integer(), nullable=True),
    sa.Column('strategy_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['session_id'], ['session.id'], ),
    sa.ForeignKeyConstraint(['strategy_id'], ['strategy.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sessionstratetgy')
    # ### end Alembic commands ###
