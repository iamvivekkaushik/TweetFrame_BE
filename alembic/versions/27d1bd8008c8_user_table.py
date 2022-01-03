"""User Table

Revision ID: 27d1bd8008c8
Revises: 
Create Date: 2021-12-28 22:30:40.811427

"""
from alembic import op
import sqlalchemy as sa
from app.enums import *
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '27d1bd8008c8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('account_id', sa.String(length=320), nullable=False),
    sa.Column('oauth_name', sa.String(length=100), nullable=False),
    sa.Column('access_token', sa.String(length=1024), nullable=False),
    sa.Column('expires_at', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(length=320), nullable=True),
    sa.Column('full_name', sa.String(length=320), nullable=True),
    sa.Column('image', sa.Text(), nullable=True),
    sa.Column('original_image', sa.Text(), nullable=True),
    sa.Column('username', sa.String(length=150), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('timezone', sa.String(length=100), nullable=True),
    sa.Column('twitter_response', sqlalchemy_utils.types.json.JSONType(), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('access_secret', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user')),
    sa.UniqueConstraint('access_token', name=op.f('uq_user_access_token')),
    sa.UniqueConstraint('access_secret', name=op.f('uq_user_access_secret')),
    sa.UniqueConstraint('username', name=op.f('uq_user_username'))
    )
    op.create_index(op.f('ix_user_account_id'), 'user', ['account_id'], unique=True)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=True)
    op.create_index(op.f('ix_user_is_active'), 'user', ['is_active'], unique=False)
    op.create_index(op.f('ix_user_oauth_name'), 'user', ['oauth_name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_oauth_name'), table_name='user')
    op.drop_index(op.f('ix_user_is_active'), table_name='user')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_account_id'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
