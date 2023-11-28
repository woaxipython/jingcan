"""empty message

Revision ID: c4e7ad522670
Revises: 076ae07de9f0
Create Date: 2023-11-21 18:38:09.102731

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c4e7ad522670'
down_revision = '076ae07de9f0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('account', schema=None) as batch_op:
        batch_op.drop_constraint('account_ibfk_2', type_='foreignkey')
        batch_op.drop_column('plat_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('account', schema=None) as batch_op:
        batch_op.add_column(sa.Column('plat_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('account_ibfk_2', 'plat', ['plat_id'], ['id'])

    # ### end Alembic commands ###
