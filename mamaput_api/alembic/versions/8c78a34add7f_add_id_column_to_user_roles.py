"""Add id column to user_roles

Revision ID: 8c78a34add7f
Revises: 24d0efaa7b2d
Create Date: 2024-12-17 00:45:20.556087

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c78a34add7f'
down_revision: Union[str, None] = '24d0efaa7b2d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order_details')
    op.drop_table('orders')
    op.drop_table('addresses')
    op.drop_table('users')
    op.drop_table('payments')
    op.drop_table('carts')
    op.drop_table('shipping_info')
    op.drop_table('user_roles')
    op.drop_table('reviews')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reviews',
                    sa.Column('review_id', sa.INTEGER(), nullable=False),
                    sa.Column('content', sa.TEXT(), nullable=True),
                    sa.Column('rating', sa.INTEGER(), nullable=False),
                    sa.Column('has_reviewed', sa.BOOLEAN(), nullable=False),
                    sa.Column('date_reviewed', sa.DATETIME(), nullable=False),
                    sa.Column('menu_id', sa.INTEGER(), nullable=True),
                    sa.Column('user_id', sa.INTEGER(), nullable=True),
                    sa.ForeignKeyConstraint(['menu_id'], ['menus.menu_id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
                    sa.PrimaryKeyConstraint('review_id')
                    )
    op.create_table('user_roles',
                    sa.Column('user_id', sa.INTEGER(), nullable=False),
                    sa.Column('role_id', sa.INTEGER(), nullable=False),
                    sa.ForeignKeyConstraint(['role_id'], ['roles.role_id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
                    sa.PrimaryKeyConstraint('user_id', 'role_id')
                    )
    op.create_table('shipping_info',
                    sa.Column('shipping_info_id',
                              sa.INTEGER(), nullable=False),
                    sa.Column('shipping_Method', sa.VARCHAR(), nullable=False),
                    sa.Column('shipping_cost', sa.FLOAT(), nullable=False),
                    sa.Column('shipping_status', sa.VARCHAR(), nullable=False),
                    sa.Column('shipped_date', sa.DATETIME(), nullable=False),
                    sa.Column('expected_delivery_date',
                              sa.DATETIME(), nullable=False),
                    sa.Column('order_id', sa.INTEGER(), nullable=True),
                    sa.Column('address_id', sa.INTEGER(), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['address_id'], ['addresses.address_id'], ),
                    sa.ForeignKeyConstraint(
                        ['order_id'], ['orders.order_id'], ),
                    sa.PrimaryKeyConstraint('shipping_info_id')
                    )

    op.create_table('carts',
                    sa.Column('cart_id', sa.INTEGER(), nullable=False),
                    sa.Column('date_created', sa.DATETIME(), nullable=False),
                    sa.Column('user_id', sa.INTEGER(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
                    sa.PrimaryKeyConstraint('cart_id')
                    )
    op.create_table('payments',
                    sa.Column('payment_id', sa.INTEGER(), nullable=False),
                    sa.Column('payment_Method', sa.VARCHAR(), nullable=False),
                    sa.Column('amount', sa.FLOAT(), nullable=False),
                    sa.Column('payment_status', sa.VARCHAR(), nullable=False),
                    sa.Column('payment_date', sa.DATETIME(), nullable=True),
                    sa.Column('reference', sa.VARCHAR(), nullable=False),
                    sa.Column('order_id', sa.INTEGER(), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['order_id'], ['orders.order_id'], ),
                    sa.PrimaryKeyConstraint('payment_id'),
                    sa.UniqueConstraint('reference')
                    )
    op.create_table('users',
                    sa.Column('user_id', sa.INTEGER(), nullable=False),
                    sa.Column('title', sa.VARCHAR(), nullable=False),
                    sa.Column('first_name', sa.VARCHAR(), nullable=False),
                    sa.Column('last_name', sa.VARCHAR(), nullable=False),
                    sa.Column('gender', sa.VARCHAR(), nullable=False),
                    sa.Column('email', sa.VARCHAR(), nullable=False),
                    sa.Column('password', sa.VARCHAR(), nullable=False),
                    sa.Column('phone', sa.INTEGER(), nullable=False),
                    sa.Column('join_date', sa.DATETIME(), nullable=True),
                    sa.Column('user_url', sa.VARCHAR(), nullable=True),
                    sa.PrimaryKeyConstraint('user_id')
                    )

    op.create_table('addresses',
                    sa.Column('address_id', sa.INTEGER(), nullable=False),
                    sa.Column('address', sa.VARCHAR(), nullable=False),
                    sa.Column('town', sa.VARCHAR(), nullable=False),
                    sa.Column('state', sa.VARCHAR(), nullable=False),
                    sa.Column('lga', sa.VARCHAR(), nullable=False),
                    sa.Column('landmark', sa.VARCHAR(), nullable=True),
                    sa.Column('user_id', sa.INTEGER(), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
                    sa.PrimaryKeyConstraint('address_id')
                    )
    op.create_table('orders',
                    sa.Column('order_id', sa.INTEGER(), nullable=False),
                    sa.Column('total_price', sa.FLOAT(), nullable=False),
                    sa.Column('date_ordered', sa.DATETIME(), nullable=False),
                    sa.Column('expected_date_of_delivery',
                              sa.DATETIME(), nullable=True),
                    sa.Column('status', sa.VARCHAR(), nullable=False),
                    sa.Column('user_id', sa.INTEGER(), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
                    sa.PrimaryKeyConstraint('order_id')
                    )
    op.create_table('order_details',
                    sa.Column('order_details_id',
                              sa.INTEGER(), nullable=False),
                    sa.Column('quantity', sa.INTEGER(), nullable=False),
                    sa.Column('discount', sa.FLOAT(), nullable=True),
                    sa.Column('price', sa.FLOAT(), nullable=False),
                    sa.Column('menu_id', sa.INTEGER(), nullable=True),
                    sa.Column('order_id', sa.INTEGER(), nullable=True),
                    sa.ForeignKeyConstraint(['menu_id'], ['menus.menu_id'], ),
                    sa.ForeignKeyConstraint(
                        ['order_id'], ['orders.order_id'], ),
                    sa.PrimaryKeyConstraint('order_details_id')
                    )
    # ### end Alembic commands ###
