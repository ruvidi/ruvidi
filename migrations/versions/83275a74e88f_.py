"""empty message

Revision ID: 83275a74e88f
Revises: e5568e948e4b
Create Date: 2022-07-20 15:00:26.508678

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83275a74e88f'
down_revision = 'e5568e948e4b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('video', sa.Column('source_url', sa.String(length=100), nullable=True))
    op.add_column('video', sa.Column('om_url', sa.String(length=100), nullable=True))
    op.drop_column('video', 'webm_url')
    op.drop_column('video', 'old_mobile_url')
    op.drop_column('video', 'mp4_url')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('video', sa.Column('mp4_url', sa.VARCHAR(length=100), nullable=True))
    op.add_column('video', sa.Column('old_mobile_url', sa.VARCHAR(length=100), nullable=True))
    op.add_column('video', sa.Column('webm_url', sa.VARCHAR(length=100), nullable=True))
    op.drop_column('video', 'om_url')
    op.drop_column('video', 'source_url')
    # ### end Alembic commands ###
