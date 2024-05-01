"""empty message

Revision ID: dacb38b02f52
Revises: 1adcde440e7d
Create Date: 2024-04-11 17:57:53.010076

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dacb38b02f52'
down_revision = '1adcde440e7d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('doctor', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role', sa.Enum('ADMIN', 'DOCTOR', 'PATIENT', name='userrole'), nullable=True))

    with op.batch_alter_table('patient', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role', sa.Enum('ADMIN', 'DOCTOR', 'PATIENT', name='userrole'), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('patient', schema=None) as batch_op:
        batch_op.drop_column('role')

    with op.batch_alter_table('doctor', schema=None) as batch_op:
        batch_op.drop_column('role')

    # ### end Alembic commands ###
