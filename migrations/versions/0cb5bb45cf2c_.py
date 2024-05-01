"""empty message

Revision ID: 0cb5bb45cf2c
Revises: a7066673b520
Create Date: 2024-04-06 15:11:58.323956

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0cb5bb45cf2c'
down_revision = 'a7066673b520'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('work_schedule',
    sa.Column('doctor_id', sa.Integer(), nullable=False),
    sa.Column('day_of_week', sa.String(length=20), nullable=False),
    sa.Column('start_time', sa.Time(), nullable=False),
    sa.Column('end_time', sa.Time(), nullable=False),
    sa.Column('id', sa.String(length=60), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['doctor_id'], ['doctor.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('doctor', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_active', sa.Boolean(), nullable=True))

    with op.batch_alter_table('education', schema=None) as batch_op:
        batch_op.alter_column('school',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('education', schema=None) as batch_op:
        batch_op.alter_column('school',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)

    with op.batch_alter_table('doctor', schema=None) as batch_op:
        batch_op.drop_column('is_active')

    op.drop_table('work_schedule')
    # ### end Alembic commands ###
