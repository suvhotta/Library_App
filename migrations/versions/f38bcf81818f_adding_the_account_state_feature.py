"""Adding the account_state feature

Revision ID: f38bcf81818f
Revises: cf7004c91a37
Create Date: 2020-04-21 17:58:44.480118

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f38bcf81818f'
down_revision = 'cf7004c91a37'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('account_state', sa.String(length=10), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'account_state')
    # ### end Alembic commands ###
