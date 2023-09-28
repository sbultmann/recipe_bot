"""first migration

Revision ID: bc363d984be4
Revises: 
Create Date: 2023-09-20 21:02:21.744734

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc363d984be4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('recipe',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('prompt', sa.Text(), nullable=True),
    sa.Column('beschreibung', sa.Text(), nullable=True),
    sa.Column('portionen', sa.Integer(), nullable=True),
    sa.Column('recipe_type', sa.String(length=64), nullable=True),
    sa.Column('image_id', sa.String(length=64), nullable=True),
    sa.Column('dish_type', sa.String(length=64), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('recipe', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_recipe_timestamp'), ['timestamp'], unique=False)
        batch_op.create_index(batch_op.f('ix_recipe_title'), ['title'], unique=False)

    op.create_table('ingredients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=140), nullable=True),
    sa.Column('unit', sa.String(length=140), nullable=True),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.Column('recipe_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipe.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('instructions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('instruction', sa.String(length=140), nullable=True),
    sa.Column('recipe_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipe.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('naehrwerte',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=140), nullable=True),
    sa.Column('unit', sa.String(length=140), nullable=True),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.Column('recipe_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipe.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('naehrwerte')
    op.drop_table('instructions')
    op.drop_table('ingredients')
    with op.batch_alter_table('recipe', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_recipe_title'))
        batch_op.drop_index(batch_op.f('ix_recipe_timestamp'))

    op.drop_table('recipe')
    # ### end Alembic commands ###