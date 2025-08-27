from alembic import op
import sqlalchemy as sa

revision = '0001_init'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'todo',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('completed', sa.Boolean(), nullable=False, server_default=sa.sql.expression.false()),
    )
    op.create_index('ix_todo_user_id', 'todo', ['user_id'])

def downgrade() -> None:
    op.drop_index('ix_todo_user_id', table_name='todo')
    op.drop_table('todo')
