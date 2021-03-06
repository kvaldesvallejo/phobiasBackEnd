"""empty message

Revision ID: c59b27db2924
Revises: 
Create Date: 2021-03-06 01:30:03.085788

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c59b27db2924'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lesson',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=10), nullable=False),
    sa.Column('phobia_description', sa.String(length=500), nullable=False),
    sa.Column('description_1', sa.String(length=500), nullable=False),
    sa.Column('img_2', sa.String(length=500), nullable=False),
    sa.Column('description_2', sa.String(length=500), nullable=False),
    sa.Column('question_2', sa.Integer(), nullable=False),
    sa.Column('description_3', sa.String(length=500), nullable=False),
    sa.Column('search_3', sa.String(length=500), nullable=False),
    sa.Column('img_4', sa.String(length=500), nullable=False),
    sa.Column('description_4', sa.String(length=500), nullable=False),
    sa.Column('question_4', sa.Integer(), nullable=False),
    sa.Column('img_5', sa.String(length=500), nullable=False),
    sa.Column('description_5', sa.String(length=500), nullable=False),
    sa.Column('question_5', sa.Integer(), nullable=False),
    sa.Column('search_5', sa.String(length=500), nullable=False),
    sa.Column('description_6', sa.String(length=500), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('feeling', sa.String(length=300), nullable=True),
    sa.Column('experience', sa.String(length=300), nullable=True),
    sa.Column('step', sa.Integer(), nullable=False),
    sa.Column('date', sa.String(length=15), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fisrt_name', sa.String(length=10), nullable=False),
    sa.Column('last_name', sa.String(length=20), nullable=False),
    sa.Column('phone_number', sa.String(length=15), nullable=False),
    sa.Column('user_name', sa.String(length=20), nullable=False),
    sa.Column('profile_picture', sa.String(length=120), nullable=True),
    sa.Column('account_type', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone_number'),
    sa.UniqueConstraint('user_name')
    )
    op.create_table('patient',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('wishfearLESS', sa.String(length=300), nullable=True),
    sa.Column('previous_help', sa.Boolean(), nullable=True),
    sa.Column('zc', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('testimonial',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('desciption', sa.String(length=300), nullable=True),
    sa.Column('testimonial_photo', sa.String(length=500), nullable=True),
    sa.Column('date', sa.String(length=15), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('therapist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('ofice_location', sa.String(length=30), nullable=False),
    sa.Column('experience', sa.String(length=500), nullable=False),
    sa.Column('languages_spoke', sa.String(length=300), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('patient_phobia',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_lesson', sa.Integer(), nullable=False),
    sa.Column('id_patient', sa.Integer(), nullable=True),
    sa.Column('question_2', sa.Integer(), nullable=True),
    sa.Column('actual_step', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_lesson'], ['lesson.id'], ),
    sa.ForeignKeyConstraint(['id_patient'], ['patient.id'], ),
    sa.ForeignKeyConstraint(['question_2'], ['question.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('patient_phobia')
    op.drop_table('therapist')
    op.drop_table('testimonial')
    op.drop_table('patient')
    op.drop_table('user')
    op.drop_table('question')
    op.drop_table('lesson')
    # ### end Alembic commands ###
