"""empty message

Revision ID: 09f591fd7969
Revises: 2325ba647ef2
Create Date: 2024-03-24 20:14:54.536484

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '09f591fd7969'
down_revision = '2325ba647ef2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('token', schema=None) as batch_op:
        batch_op.alter_column('user_email',
               existing_type=mysql.VARCHAR(length=20),
               type_=sa.String(length=50),
               existing_nullable=False)
        batch_op.alter_column('email_token',
               existing_type=mysql.VARCHAR(length=30),
               type_=sa.String(length=100),
               existing_nullable=True)
        batch_op.alter_column('password_token',
               existing_type=mysql.VARCHAR(length=30),
               type_=sa.String(length=100),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('token', schema=None) as batch_op:
        batch_op.alter_column('password_token',
               existing_type=sa.String(length=100),
               type_=mysql.VARCHAR(length=30),
               existing_nullable=True)
        batch_op.alter_column('email_token',
               existing_type=sa.String(length=100),
               type_=mysql.VARCHAR(length=30),
               existing_nullable=True)
        batch_op.alter_column('user_email',
               existing_type=sa.String(length=50),
               type_=mysql.VARCHAR(length=20),
               existing_nullable=False)

    # ### end Alembic commands ###