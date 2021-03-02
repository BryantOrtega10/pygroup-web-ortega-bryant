"""I add users table and Rol table

Revision ID: 86d99681e6ba
Revises: 
Create Date: 2020-12-20 19:10:31.522709

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86d99681e6ba'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('rol_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'user', 'rol', ['rol_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'rol_id')
    # ### end Alembic commands ###