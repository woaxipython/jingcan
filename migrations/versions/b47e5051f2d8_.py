"""empty message

Revision ID: b47e5051f2d8
Revises: 6a9cf9ac7095
Create Date: 2023-11-27 11:10:10.236615

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b47e5051f2d8'
down_revision = '6a9cf9ac7095'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pvcontent', schema=None) as batch_op:
        batch_op.add_column(sa.Column('search_id', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('title', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('content_id', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('desc', sa.String(length=500), nullable=True))
        batch_op.add_column(sa.Column('liked', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('collected', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('commented', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('forwarded', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('content_link', sa.String(length=200), nullable=True))
        batch_op.add_column(sa.Column('video_link', sa.String(length=200), nullable=True))
        batch_op.add_column(sa.Column('imageList', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('contenttype', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('spyder_url', sa.String(length=200), nullable=True))
        batch_op.add_column(sa.Column('status', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('attention', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('upload_time', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('upgrade_time', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('create_time', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('account_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('goods_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'group', ['goods_id'], ['id'])
        batch_op.create_foreign_key(None, 'account', ['account_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pvcontent', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('goods_id')
        batch_op.drop_column('account_id')
        batch_op.drop_column('create_time')
        batch_op.drop_column('upgrade_time')
        batch_op.drop_column('upload_time')
        batch_op.drop_column('attention')
        batch_op.drop_column('status')
        batch_op.drop_column('spyder_url')
        batch_op.drop_column('contenttype')
        batch_op.drop_column('imageList')
        batch_op.drop_column('video_link')
        batch_op.drop_column('content_link')
        batch_op.drop_column('forwarded')
        batch_op.drop_column('commented')
        batch_op.drop_column('collected')
        batch_op.drop_column('liked')
        batch_op.drop_column('desc')
        batch_op.drop_column('content_id')
        batch_op.drop_column('title')
        batch_op.drop_column('search_id')

    # ### end Alembic commands ###