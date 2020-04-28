"""Adding the Date of Issue column to booksissued table

Revision ID: bfd3b0147ff2
Revises: f50465ab5cf1
Create Date: 2020-04-28 20:37:03.880755

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bfd3b0147ff2'
down_revision = 'f50465ab5cf1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books_issued', sa.Column('issue_date', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('books_issued', 'issue_date')
    # ### end Alembic commands ###