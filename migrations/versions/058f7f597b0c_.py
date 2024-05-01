"""empty message

Revision ID: 058f7f597b0c
Revises: 319859dadf79
Create Date: 2024-03-26 17:29:55.919610

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '058f7f597b0c'
down_revision = '319859dadf79'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('patient', schema=None) as batch_op:
        batch_op.add_column(sa.Column('age', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('patient', schema=None) as batch_op:
        batch_op.drop_column('age')

    # ### end Alembic commands ###
