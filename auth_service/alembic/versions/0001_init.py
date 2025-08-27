from alembic import op
import sqlalchemy as sa

revision = '0001_init'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'user',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(), nullable=False),
    )
    op.create_index('ix_user_email', 'user', ['email'], unique=True)

def downgrade() -> None:
    op.drop_index('ix_user_email', table_name='user')
    op.drop_table('user')
