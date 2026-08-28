"""normalize table names to lowercase

Revision ID: 0003_lowercase_tables
Revises: 0002_priority
Create Date: 2026-08-27 23:21:01.139029

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0003_lowercase_tables'
down_revision = '0002_priority'
branch_labels = None
depends_on = None


def upgrade():
    category_table = _find_table_name('category')
    youtube_link_table = _find_table_name('youtubelink')

    if category_table != 'category':
        op.rename_table(category_table, 'category')
    if youtube_link_table != 'youtubelink':
        op.rename_table(youtube_link_table, 'youtubelink')


def downgrade():
    if _mysql_uses_case_sensitive_table_names():
        op.rename_table('youtubelink', 'youTubeLink')
        op.rename_table('category', 'Category')


def _mysql_uses_case_sensitive_table_names():
    connection = op.get_bind()
    if connection.dialect.name != 'mysql':
        return False

    lower_case_table_names = connection.execute(
        sa.text('SELECT @@lower_case_table_names')
    ).scalar()
    return lower_case_table_names == 0


def _find_table_name(expected_name):
    table_names = sa.inspect(op.get_bind()).get_table_names()
    for table_name in table_names:
        if table_name.lower() == expected_name.lower():
            return table_name

    raise RuntimeError("Expected table '{}' was not found.".format(expected_name))
