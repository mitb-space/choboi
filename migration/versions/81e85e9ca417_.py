"""empty message

Revision ID: 81e85e9ca417
Revises: initial messages table
Create Date: 2020-03-13 23:00:33.340390

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81e85e9ca417'
down_revision = 'eca60912b1a9'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('channel_id', sa.String(), nullable=False),
        sa.Column('message', sa.Text()),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
    )


def downgrade():
    op.drop_table('messages')
