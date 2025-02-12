"""empty message

Revision ID: 2b97328f9f8f
Revises: 99edfe497855
Create Date: 2023-07-27 10:54:41.146852

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import update, MetaData


# revision identifiers, used by Alembic.
revision = '2b97328f9f8f'
down_revision = '99edfe497855'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.add_column(sa.Column('website_link', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('genres', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('seeking_talent', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('seeking_talent_description', sa.String(length=500), nullable=True))

    # The statement being executed needs to be in single quotes because the name of the table needs to be double quoted because it has an uppercase character
    # But text we're setting in the genres field needs to be single quoted, which can't be done if the whole statement is single quoted. So we need to create
    # a formatted string that takes in the single quoted value
    # Yeesh. Don't name tables with upper cases
    v = "'[]'"
    op.execute(f'UPDATE "Venue" SET genres={v} WHERE genres is NULL')
    op.execute('UPDATE "Venue" SET seeking_talent=FALSE WHERE seeking_talent is NULL')
    
    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.alter_column('genres',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('seeking_talent',
               existing_type=sa.Boolean(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.drop_column('seeking_talent_description')
        batch_op.drop_column('seeking_talent')
        batch_op.drop_column('genres')
        batch_op.drop_column('website_link')

    # ### end Alembic commands ###
