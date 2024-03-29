"""position added

Revision ID: c84f3ab06276
Revises: a46666d95eca
Create Date: 2019-06-20 17:54:17.253633

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c84f3ab06276'
down_revision = 'a46666d95eca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('position',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('asset', sa.String(length=6), nullable=True),
    sa.Column('dtisoll', sa.String(length=20), nullable=True),
    sa.Column('dtosoll', sa.String(length=20), nullable=True),
    sa.Column('dtiist', sa.String(length=20), nullable=True),
    sa.Column('dtoist', sa.String(length=20), nullable=True),
    sa.Column('bi', sa.Float(), nullable=True),
    sa.Column('bo', sa.Float(), nullable=True),
    sa.Column('ai', sa.Float(), nullable=True),
    sa.Column('ao', sa.Float(), nullable=True),
    sa.Column('groisoll', sa.Float(), nullable=True),
    sa.Column('groiist', sa.Float(), nullable=True),
    sa.Column('roisoll', sa.Float(), nullable=True),
    sa.Column('roiist', sa.Float(), nullable=True),
    sa.Column('returns', sa.Float(), nullable=True),
    sa.Column('espread', sa.Float(), nullable=True),
    sa.Column('spread', sa.Float(), nullable=True),
    sa.Column('lots', sa.Float(), nullable=True),
    sa.Column('p_mc', sa.Float(), nullable=True),
    sa.Column('p_md', sa.Float(), nullable=True),
    sa.Column('slfalg', sa.Boolean(), nullable=True),
    sa.Column('ticksdiff', sa.Integer(), nullable=True),
    sa.Column('nofext', sa.Integer(), nullable=True),
    sa.Column('direction', sa.Integer(), nullable=True),
    sa.Column('closed', sa.Boolean(), nullable=True),
    sa.Column('strategyname', sa.String(length=64), nullable=True),
    sa.Column('filename', sa.String(length=40), nullable=True),
    sa.Column('filecontent', sa.LargeBinary(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('position')
    # ### end Alembic commands ###
