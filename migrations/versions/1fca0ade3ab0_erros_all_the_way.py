"""erros all the way

Revision ID: 1fca0ade3ab0
Revises: e2505eb05ec0
Create Date: 2019-04-30 11:42:51.597872

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1fca0ade3ab0'
down_revision = 'e2505eb05ec0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('request_id_fkey', 'request', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('request_id_fkey', 'request', 'tablemodel', ['id'], ['id'])
    # ### end Alembic commands ###
