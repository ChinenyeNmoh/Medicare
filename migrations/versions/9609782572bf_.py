"""empty message

Revision ID: 9609782572bf
Revises: 9fe85e8cb9f6
Create Date: 2024-04-14 17:19:40.813252

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9609782572bf'
down_revision = '9fe85e8cb9f6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('doctor', schema=None) as batch_op:
        batch_op.add_column(sa.Column('consultation_fee', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('doctor', schema=None) as batch_op:
        batch_op.drop_column('consultation_fee')

    # ### end Alembic commands ###
