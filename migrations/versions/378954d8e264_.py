"""empty message

Revision ID: 378954d8e264
Revises: 688a4f7bcb8b
Create Date: 2023-11-27 11:08:24.004784

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '378954d8e264'
down_revision = '688a4f7bcb8b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pvcontent', schema=None) as batch_op:
        batch_op.drop_constraint('pvcontent_ibfk_4', type_='foreignkey')
        batch_op.drop_constraint('pvcontent_ibfk_3', type_='foreignkey')
        batch_op.drop_constraint('pvcontent_ibfk_2', type_='foreignkey')
        batch_op.create_foreign_key(None, 'group', ['goods_id'], ['id'])
        batch_op.drop_column('output_id')
        batch_op.drop_column('promotion_id')
        batch_op.drop_column('prtype_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pvcontent', schema=None) as batch_op:
        batch_op.add_column(sa.Column('prtype_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('promotion_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('output_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('pvcontent_ibfk_2', 'output_mode', ['output_id'], ['id'])
        batch_op.create_foreign_key('pvcontent_ibfk_3', 'promotion', ['promotion_id'], ['id'])
        batch_op.create_foreign_key('pvcontent_ibfk_4', 'prtype', ['prtype_id'], ['id'])

    # ### end Alembic commands ###
