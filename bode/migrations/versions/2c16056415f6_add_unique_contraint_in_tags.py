"""Add unique contraint in tags

Revision ID: 2c16056415f6
Revises: a1d5f4b5886f
Create Date: 2022-04-18 19:00:06.554077

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "2c16056415f6"
down_revision = "a1d5f4b5886f"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(
        "_task_id_name_uc", "tags", ["task_id", "name"]
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("_task_id_name_uc", "tags", type_="unique")
    # ### end Alembic commands ###
