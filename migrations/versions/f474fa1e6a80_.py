"""empty message

Revision ID: f474fa1e6a80
Revises: 08c37364dd87
Create Date: 2023-11-27 12:39:01.798134

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f474fa1e6a80'
down_revision = '08c37364dd87'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pvcontent', schema=None) as batch_op:
        batch_op.drop_index('content_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pvcontent', schema=None) as batch_op:
        batch_op.create_index('content_id', ['content_id'], unique=False)

    # ### end Alembic commands ###
