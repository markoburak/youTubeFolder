"""expand category emoji to text

Revision ID: 0004_category_emoji_text
Revises: 0003_lowercase_tables
Create Date: 2026-08-27 23:21:42.084001

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0004_category_emoji_text'
down_revision = '0003_lowercase_tables'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        'category',
        'emoji',
        existing_type=sa.String(length=10),
        type_=sa.Text(),
        existing_nullable=True,
    )


def downgrade():
    op.alter_column(
        'category',
        'emoji',
        existing_type=sa.Text(),
        type_=sa.String(length=10),
        existing_nullable=True,
    )
