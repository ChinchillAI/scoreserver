"""test revision

Revision ID: d40953d49a76
Revises: 
Create Date: 2024-08-26 00:04:43.039897

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = 'd40953d49a76'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('highscore',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('score', sa.Integer(), nullable=False),
    sa.Column('owner_id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('highscore')
    op.drop_table('user')
    # ### end Alembic commands ###
