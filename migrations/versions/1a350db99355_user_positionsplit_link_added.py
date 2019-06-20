"""user-positionSplit link added

Revision ID: 1a350db99355
Revises: 047e92892876
Create Date: 2019-06-20 17:59:11.180740

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a350db99355'
down_revision = '047e92892876'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('positionsplit', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'positionsplit', 'user', ['owner_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'positionsplit', type_='foreignkey')
    op.drop_column('positionsplit', 'owner_id')
    # ### end Alembic commands ###