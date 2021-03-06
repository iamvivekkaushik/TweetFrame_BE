"""Added File Table

Revision ID: ae52bca8aeac
Revises: e42e939edaa8
Create Date: 2022-01-05 21:47:40.850096

"""
from alembic import op
import sqlalchemy as sa
from app.enums import *
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'ae52bca8aeac'
down_revision = 'e42e939edaa8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('file',
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('url', sa.Text(), nullable=False),
    sa.Column('path', sa.Text(), nullable=False),
    sa.Column('mimetype', sa.String(length=50), nullable=False),
    sa.Column('size', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_file'))
    )
    op.create_index(op.f('ix_file_id'), 'file', ['id'], unique=False)
    op.create_index(op.f('ix_file_is_active'), 'file', ['is_active'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_file_is_active'), table_name='file')
    op.drop_index(op.f('ix_file_id'), table_name='file')
    op.drop_table('file')
    # ### end Alembic commands ###
