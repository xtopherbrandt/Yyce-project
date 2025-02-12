"""empty message

Revision ID: c50dc71b5ee3
Revises: 2b97328f9f8f
Create Date: 2023-08-09 11:29:29.138066

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c50dc71b5ee3'
down_revision = '2b97328f9f8f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.add_column(sa.Column('website_link', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('seeking_venue', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('seeking_description', sa.String(length=500), nullable=True))

    op.execute('UPDATE "Artist" SET seeking_venue=FALSE WHERE seeking_venue is NULL')
    
    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.alter_column('seeking_venue',
               existing_type=sa.Boolean(),
               nullable=False)
        
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.drop_column('seeking_description')
        batch_op.drop_column('seeking_venue')
        batch_op.drop_column('website_link')

    # ### end Alembic commands ###
