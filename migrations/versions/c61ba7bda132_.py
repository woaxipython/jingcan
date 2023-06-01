"""empty message

Revision ID: c61ba7bda132
Revises: cb58df7342d9
Create Date: 2023-05-31 18:56:22.980554

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c61ba7bda132'
down_revision = 'cb58df7342d9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sale', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cost', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sale', schema=None) as batch_op:
        batch_op.drop_column('cost')

    # ### end Alembic commands ###
