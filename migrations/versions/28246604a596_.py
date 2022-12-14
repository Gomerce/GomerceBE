"""empty message

Revision ID: 28246604a596
Revises: 2a28bfdff6f2
Create Date: 2022-12-02 16:04:58.685594

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28246604a596'
down_revision = '2a28bfdff6f2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('carts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('unit_price', sa.Float(), nullable=False),
    sa.Column('quantity', sa.Float(), nullable=False),
    sa.Column('total_cost', sa.Float(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('carts')
    # ### end Alembic commands ###
