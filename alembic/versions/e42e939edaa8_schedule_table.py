"""Schedule Table

Revision ID: e42e939edaa8
Revises: 7070844f842a
Create Date: 2021-12-28 22:32:34.392878

"""
from alembic import op
import sqlalchemy as sa
from app.enums import *
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'e42e939edaa8'
down_revision = '7070844f842a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('schedule',
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=320), nullable=False),
    sa.Column('type', sa.String(length=20), nullable=False),
    sa.Column('schedule_type', sa.String(length=20), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.Column('settings', sqlalchemy_utils.types.json.JSONType(), nullable=False),
    sa.Column('message', sa.Text(), nullable=True),
    sa.Column('start_date', sa.Date(), nullable=True),
    sa.Column('end_date', sa.Date(), nullable=True),
    sa.Column('start_time', sa.String(length=20), nullable=True),
    sa.Column('end_time', sa.String(length=20), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('frame_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['frame_id'], ['frame.id'], name=op.f('fk_schedule_frame_id_frame')),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_schedule_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_schedule'))
    )
    op.create_index(op.f('ix_schedule_id'), 'schedule', ['id'], unique=False)
    op.create_index(op.f('ix_schedule_is_active'), 'schedule', ['is_active'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_schedule_is_active'), table_name='schedule')
    op.drop_index(op.f('ix_schedule_id'), table_name='schedule')
    op.drop_table('schedule')
    # ### end Alembic commands ###
