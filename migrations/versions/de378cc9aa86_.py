"""empty message

Revision ID: de378cc9aa86
Revises: c4e7ad522670
Create Date: 2023-11-21 18:38:45.063711

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'de378cc9aa86'
down_revision = 'c4e7ad522670'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('account', schema=None) as batch_op:
        batch_op.add_column(sa.Column('plat_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'plat', ['plat_id'], ['id'])

    with op.batch_alter_table('pvcontent', schema=None) as batch_op:
        batch_op.drop_constraint('pvcontent_ibfk_5', type_='foreignkey')
        batch_op.drop_column('plat_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pvcontent', schema=None) as batch_op:
        batch_op.add_column(sa.Column('plat_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('pvcontent_ibfk_5', 'plat', ['plat_id'], ['id'])

    with op.batch_alter_table('account', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('plat_id')

    # ### end Alembic commands ###