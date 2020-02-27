"""votes

Revision ID: eca60912b1a9
Revises: initial votes table
Create Date: 2020-02-26 13:40:01.403640

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eca60912b1a9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'votes',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('giver_id', sa.String(), nullable=False),
        sa.Column('recipient_id', sa.String()),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
        sa.Column('amount', sa.Integer))

def downgrade():
    op.drop_table('votes')
