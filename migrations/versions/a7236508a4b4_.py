"""empty message

Revision ID: a7236508a4b4
Revises: fb8f6ab7c541
Create Date: 2021-03-18 00:02:35.897257

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a7236508a4b4'
down_revision = 'fb8f6ab7c541'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('therapist', sa.Column('phobia', sa.String(length=500), nullable=False))
    op.add_column('therapist', sa.Column('zipcode', sa.String(length=30), nullable=False))
    op.drop_column('therapist', 'ofice_location')
    op.drop_column('therapist', 'experience')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('therapist', sa.Column('experience', mysql.VARCHAR(length=500), nullable=False))
    op.add_column('therapist', sa.Column('ofice_location', mysql.VARCHAR(length=30), nullable=False))
    op.drop_column('therapist', 'zipcode')
    op.drop_column('therapist', 'phobia')
    # ### end Alembic commands ###