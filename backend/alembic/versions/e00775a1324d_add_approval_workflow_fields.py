from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'e00775a1324d'
down_revision = 'e6e85f5c45d7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'assessments',
        sa.Column('status', sa.String(), server_default='pending')
    )
    op.add_column(
        'assessments',
        sa.Column('insight', sa.Text(), nullable=True)
    )
    op.add_column(
        'assessments',
        sa.Column('recommendation', sa.Text(), nullable=True)
    )
    op.add_column(
        'assessments',
        sa.Column('doctor_notes', sa.Text(), nullable=True)
    )
    op.add_column(
        'assessments',
        sa.Column('approved_at', sa.DateTime(), nullable=True)
    )


def downgrade():
    op.drop_column('assessments', 'approved_at')
    op.drop_column('assessments', 'doctor_notes')
    op.drop_column('assessments', 'recommendation')
    op.drop_column('assessments', 'insight')
    op.drop_column('assessments', 'status')