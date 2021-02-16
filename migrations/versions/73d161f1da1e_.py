"""empty message

Revision ID: 73d161f1da1e
Revises: 5bcecbac0181
Create Date: 2021-02-12 20:34:56.967830

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '73d161f1da1e'
down_revision = '5bcecbac0181'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('contact', 'password_hash',
               existing_type=mysql.VARCHAR(length=250),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('contact', 'password_hash',
               existing_type=mysql.VARCHAR(length=250),
               nullable=False)
    # ### end Alembic commands ###