"""Created one-to-many relationship

Revision ID: f41b12facd87
Revises: badd7e2d8837
Create Date: 2023-01-03 13:48:40.213820

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f41b12facd87'
down_revision = 'badd7e2d8837'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('complaint_table', schema=None) as batch_op:
        batch_op.add_column(sa.Column('complainer_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'complainer_table', ['complainer_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('complaint_table', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('complainer_id')

    # ### end Alembic commands ###
