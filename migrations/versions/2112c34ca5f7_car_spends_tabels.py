"""Car spends tabels

Revision ID: 2112c34ca5f7
Revises: 38b523f13530
Create Date: 2019-11-17 14:25:25.853042

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2112c34ca5f7'
down_revision = '38b523f13530'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('car_spend_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=140), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_car_spend_type_type'), 'car_spend_type', ['type'], unique=False)
    op.create_table('car_spend',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('trip', sa.Integer(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('car_id', sa.Integer(), nullable=True),
    sa.Column('car_spend_type_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['car_id'], ['car.id'], ),
    sa.ForeignKeyConstraint(['car_spend_type_id'], ['car_spend_type.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_car_spend_timestamp'), 'car_spend', ['timestamp'], unique=False)
    op.add_column('car', sa.Column('buy_price', sa.Float(), nullable=True))
    op.add_column('car', sa.Column('buy_time', sa.DateTime(), nullable=True))
    op.add_column('car', sa.Column('sale_time', sa.DateTime(), nullable=True))
    op.add_column('car', sa.Column('start_trip', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_car_sale_time'), 'car', ['sale_time'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_car_sale_time'), table_name='car')
    op.drop_column('car', 'start_trip')
    op.drop_column('car', 'sale_time')
    op.drop_column('car', 'buy_time')
    op.drop_column('car', 'buy_price')
    op.drop_index(op.f('ix_car_spend_timestamp'), table_name='car_spend')
    op.drop_table('car_spend')
    op.drop_index(op.f('ix_car_spend_type_type'), table_name='car_spend_type')
    op.drop_table('car_spend_type')
    # ### end Alembic commands ###
