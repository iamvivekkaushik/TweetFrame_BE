"""Purchase table

Revision ID: 43a8368b5e49
Revises: f39ee9e6e355
Create Date: 2021-12-25 22:11:04.944231

"""
from alembic import op
import sqlalchemy as sa
import fastapi_users
import fastapi_users_db_sqlalchemy
from app.enums import *
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '43a8368b5e49'
down_revision = 'f39ee9e6e355'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('purchase',
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('remaining_custom_frames', sa.Integer(), nullable=False),
    sa.Column('remaining_frame_usage', sa.Integer(), nullable=False),
    sa.Column('remaining_active_schedules', sa.Integer(), nullable=False),
    sa.Column('start_date', sa.Date(), nullable=True),
    sa.Column('end_date', sa.Date(), nullable=True),
    sa.Column('start_time', sa.Text(), nullable=True),
    sa.Column('end_time', sa.Text(), nullable=True),
    sa.Column('user_id', fastapi_users_db_sqlalchemy.GUID(), nullable=True),
    sa.Column('plan_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['plan_id'], ['plan.id'], name=op.f('fk_purchase_plan_id_plan')),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_purchase_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_purchase'))
    )
    op.create_index(op.f('ix_purchase_id'), 'purchase', ['id'], unique=False)
    op.create_index(op.f('ix_purchase_is_active'), 'purchase', ['is_active'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_purchase_is_active'), table_name='purchase')
    op.drop_index(op.f('ix_purchase_id'), table_name='purchase')
    op.drop_table('purchase')
    # ### end Alembic commands ###
