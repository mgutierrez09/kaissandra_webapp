"""asset added

Revision ID: 76affcf8b224
Revises: 
Create Date: 2019-06-20 17:47:44.814130

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76affcf8b224'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('asset',
    sa.Column('assetname', sa.String(length=6), nullable=False),
    sa.PrimaryKeyConstraint('assetname')
    )
    op.create_index(op.f('ix_asset_assetname'), 'asset', ['assetname'], unique=True)
    op.create_table('network',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('networkname', sa.String(length=64), nullable=True),
    sa.Column('weightsfile', sa.String(length=30), nullable=True),
    sa.Column('epoch', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_network_networkname'), 'network', ['networkname'], unique=True)
    op.create_table('strategy',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('strategyname', sa.String(length=64), nullable=True),
    sa.Column('spreadthr', sa.Float(), nullable=True),
    sa.Column('mcthr', sa.Float(), nullable=True),
    sa.Column('mdthr', sa.Float(), nullable=True),
    sa.Column('diropts', sa.String(length=4), nullable=True),
    sa.Column('slthr', sa.Float(), nullable=True),
    sa.Column('extthr', sa.Float(), nullable=True),
    sa.Column('poslots', sa.Float(), nullable=True),
    sa.Column('phaseshift', sa.Integer(), nullable=True),
    sa.Column('oraclename', sa.String(length=64), nullable=True),
    sa.Column('mw', sa.Integer(), nullable=True),
    sa.Column('nexs', sa.Integer(), nullable=True),
    sa.Column('og', sa.Float(), nullable=True),
    sa.Column('symbol', sa.String(length=3), nullable=True),
    sa.Column('combine', sa.String(length=5), nullable=True),
    sa.Column('combineparams', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_strategy_oraclename'), 'strategy', ['oraclename'], unique=True)
    op.create_index(op.f('ix_strategy_strategyname'), 'strategy', ['strategyname'], unique=True)
    op.create_table('trader',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tradername', sa.String(length=64), nullable=True),
    sa.Column('machine', sa.String(length=64), nullable=True),
    sa.Column('magicnumber', sa.Integer(), nullable=True),
    sa.Column('budget', sa.Float(), nullable=True),
    sa.Column('performance', sa.Float(), nullable=True),
    sa.Column('datecreated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_trader_machine'), 'trader', ['machine'], unique=False)
    op.create_index(op.f('ix_trader_magicnumber'), 'trader', ['magicnumber'], unique=False)
    op.create_index(op.f('ix_trader_tradername'), 'trader', ['tradername'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('isadmin', sa.Boolean(), nullable=True),
    sa.Column('userid', sa.String(length=20), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('firstname', sa.String(length=64), nullable=True),
    sa.Column('surname', sa.String(length=64), nullable=True),
    sa.Column('address', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('datecreated', sa.DateTime(), nullable=True),
    sa.Column('budget', sa.Float(), nullable=True),
    sa.Column('token', sa.String(length=32), nullable=True),
    sa.Column('token_expiration', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_address'), 'user', ['address'], unique=False)
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_firstname'), 'user', ['firstname'], unique=False)
    op.create_index(op.f('ix_user_surname'), 'user', ['surname'], unique=False)
    op.create_index(op.f('ix_user_token'), 'user', ['token'], unique=True)
    op.create_index(op.f('ix_user_userid'), 'user', ['userid'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('oraclenetwork',
    sa.Column('strategy_id', sa.Integer(), nullable=True),
    sa.Column('network_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['network_id'], ['network.id'], ),
    sa.ForeignKeyConstraint(['strategy_id'], ['strategy.id'], )
    )
    op.create_table('traderstratetgy',
    sa.Column('trader_id', sa.Integer(), nullable=True),
    sa.Column('strategy_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['strategy_id'], ['strategy.id'], ),
    sa.ForeignKeyConstraint(['trader_id'], ['trader.id'], )
    )
    op.create_table('usertrader',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('trader_id', sa.Integer(), nullable=False),
    sa.Column('budget', sa.Float(), nullable=True),
    sa.Column('leverage', sa.Float(), nullable=True),
    sa.Column('poslots', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['trader_id'], ['trader.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'trader_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('usertrader')
    op.drop_table('traderstratetgy')
    op.drop_table('oraclenetwork')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_userid'), table_name='user')
    op.drop_index(op.f('ix_user_token'), table_name='user')
    op.drop_index(op.f('ix_user_surname'), table_name='user')
    op.drop_index(op.f('ix_user_firstname'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_index(op.f('ix_user_address'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_trader_tradername'), table_name='trader')
    op.drop_index(op.f('ix_trader_magicnumber'), table_name='trader')
    op.drop_index(op.f('ix_trader_machine'), table_name='trader')
    op.drop_table('trader')
    op.drop_index(op.f('ix_strategy_strategyname'), table_name='strategy')
    op.drop_index(op.f('ix_strategy_oraclename'), table_name='strategy')
    op.drop_table('strategy')
    op.drop_index(op.f('ix_network_networkname'), table_name='network')
    op.drop_table('network')
    op.drop_index(op.f('ix_asset_assetname'), table_name='asset')
    op.drop_table('asset')
    # ### end Alembic commands ###
