"""logmessage added

Revision ID: 883ea4369578
Revises: af4a3c1a7872
Create Date: 2020-03-03 14:35:24.866519

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '883ea4369578'
down_revision = 'af4a3c1a7872'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('logmessage',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('datetime', sa.DateTime(), nullable=True),
    sa.Column('origin', sa.String(length=10), nullable=True),
    sa.Column('asset', sa.String(length=6), nullable=True),
    sa.Column('message', sa.String(length=300), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('logmessage')
    # ### end Alembic commands ###
