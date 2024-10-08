"""empty message

Revision ID: 3d43f6726347
Revises: 
Create Date: 2024-04-07 17:31:27.552466

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d43f6726347'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('member',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=45), nullable=False),
    sa.Column('last_name', sa.String(length=45), nullable=True),
    sa.Column('phone_number', sa.String(length=20), nullable=False),
    sa.Column('is_trainer', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone_number')
    )
    op.create_table('session',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('session_name', sa.String(length=100), nullable=False),
    sa.Column('session_date', sa.Date(), nullable=False),
    sa.Column('member_id', sa.Integer(), nullable=False),
    sa.Column('is_publish', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['member_id'], ['member.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('member_session',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('member_id', sa.Integer(), nullable=False),
    sa.Column('session_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['member_id'], ['member.id'], ),
    sa.ForeignKeyConstraint(['session_id'], ['session.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('member_session')
    op.drop_table('session')
    op.drop_table('member')
    # ### end Alembic commands ###
