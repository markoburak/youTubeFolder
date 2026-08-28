"""add priority flag to youtube links

Revision ID: 0002_priority
Revises: 0001_initial
Create Date: 2026-08-27 23:18:52.388628

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0002_priority'
down_revision = '0001_initial'
branch_labels = None
depends_on = None


def upgrade():
    youtube_link_table = _find_table_name('youtubelink')
    op.add_column(
        youtube_link_table,
        sa.Column(
            'is_priority',
            sa.Boolean(),
            server_default=sa.text('0'),
            nullable=False,
        ),
    )


def downgrade():
    op.drop_column(_find_table_name('youtubelink'), 'is_priority')


def _find_table_name(expected_name):
    table_names = sa.inspect(op.get_bind()).get_table_names()
    for table_name in table_names:
        if table_name.lower() == expected_name.lower():
            return table_name

    raise RuntimeError("Expected table '{}' was not found.".format(expected_name))
