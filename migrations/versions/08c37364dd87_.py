"""empty message

Revision ID: 08c37364dd87
Revises: 3aa19123d742
Create Date: 2023-11-27 12:37:30.072253

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '08c37364dd87'
down_revision = '3aa19123d742'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('account', schema=None) as batch_op:
        batch_op.drop_index('account_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('account', schema=None) as batch_op:
        batch_op.create_index('account_id', ['account_id'], unique=False)

    # ### end Alembic commands ###