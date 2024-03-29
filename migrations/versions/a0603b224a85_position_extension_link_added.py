"""position-extension link added

Revision ID: a0603b224a85
Revises: 5d0f9418f797
Create Date: 2019-06-20 17:56:18.674586

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0603b224a85'
down_revision = '5d0f9418f797'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('extension', sa.Column('position_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'extension', 'position', ['position_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'extension', type_='foreignkey')
    op.drop_column('extension', 'position_id')
    # ### end Alembic commands ###
