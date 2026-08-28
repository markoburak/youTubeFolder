"""initial schema

Revision ID: 0001_initial
Revises: 
Create Date: 2026-08-27 23:18:49.015645

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=150), nullable=True),
        sa.Column('password', sa.String(length=150), nullable=True),
        sa.Column('first_name', sa.String(length=150), nullable=True),
        sa.Column('last_name', sa.String(length=150), nullable=True),
        sa.Column('created_date', sa.Date(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
    )
    op.create_table(
        'Category',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('starred', sa.Boolean(), nullable=True),
        sa.Column('name', sa.String(length=50), nullable=True),
        sa.Column('emoji', sa.String(length=10), nullable=True),
        sa.Column('created_date', sa.Date(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'youTubeLink',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('url', sa.String(length=400), nullable=True),
        sa.Column('img_url', sa.String(length=400), nullable=True),
        sa.Column('title', sa.String(length=400), nullable=True),
        sa.Column('created_date', sa.Date(), nullable=True),
        sa.Column('category_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['category_id'], ['Category.id']),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    op.drop_table('youTubeLink')
    op.drop_table('Category')
    op.drop_table('user')
