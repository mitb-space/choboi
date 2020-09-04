"""create one piece chapters table

Revision ID: e60e32209ce9
Revises: 81e85e9ca417
Create Date: 2020-09-04 00:03:37.157305

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e60e32209ce9'
down_revision = '81e85e9ca417'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'one_piece_chapters',
        sa.Column('chapter', sa.Integer, primary_key=True),
        sa.Column('link', sa.String(), nullable=False),
    )


def downgrade():
    op.drop_table('one_piece_chapters')
