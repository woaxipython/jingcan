"""empty message

Revision ID: 7c8bd9589495
Revises: 3958b9b97a1e
Create Date: 2023-11-19 15:11:44.112847

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c8bd9589495'
down_revision = '3958b9b97a1e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('dyToken', schema=None) as batch_op:
        batch_op.add_column(sa.Column('wechat', sa.String(length=30), nullable=False))
        batch_op.create_unique_constraint(None, ['wechat'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('dyToken', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('wechat')

    # ### end Alembic commands ###