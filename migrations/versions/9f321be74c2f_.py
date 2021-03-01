"""empty message

Revision ID: 9f321be74c2f
Revises: 762402052503
Create Date: 2021-02-28 20:48:15.672479

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9f321be74c2f'
down_revision = '762402052503'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('account_type', sa.Integer(), nullable=False))
    op.add_column('user', sa.Column('fisrt_name', sa.String(length=10), nullable=False))
    op.add_column('user', sa.Column('last_name', sa.String(length=20), nullable=False))
    op.add_column('user', sa.Column('phone_numbrer', sa.Integer(), nullable=False))
    op.add_column('user', sa.Column('profile_picture', sa.String(length=120), nullable=True))
    op.add_column('user', sa.Column('user_name', sa.String(length=20), nullable=False))
    op.create_unique_constraint(None, 'user', ['phone_numbrer'])
    op.create_unique_constraint(None, 'user', ['user_name'])
    op.drop_column('user', 'is_active')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_active', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_column('user', 'user_name')
    op.drop_column('user', 'profile_picture')
    op.drop_column('user', 'phone_numbrer')
    op.drop_column('user', 'last_name')
    op.drop_column('user', 'fisrt_name')
    op.drop_column('user', 'account_type')
    # ### end Alembic commands ###
