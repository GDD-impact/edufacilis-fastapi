"""added more models

Revision ID: bc8a30f66b53
Revises: d66c34bb0eb3
Create Date: 2025-04-02 01:39:27.522426

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bc8a30f66b53'
down_revision: Union[str, None] = 'd66c34bb0eb3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('teachers',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('classes', sa.JSON(), nullable=False),
    sa.Column('subjects', sa.JSON(), nullable=False),
    sa.Column('school', sa.String(), nullable=False),
    sa.Column('school_location', sa.String(), nullable=False),
    sa.Column('is_form_teacher', sa.Boolean(), nullable=True),
    sa.Column('my_class', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('subject_teachers_classes',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('class_name', sa.String(), nullable=False),
    sa.Column('class_type', sa.String(), nullable=False),
    sa.Column('academic_session', sa.String(), nullable=False),
    sa.Column('subject_name', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('teacher_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['teacher_id'], ['teachers.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('teachers_classes',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('class_name', sa.String(), nullable=False),
    sa.Column('class_type', sa.String(), nullable=False),
    sa.Column('academic_session', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('teacher_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['teacher_id'], ['teachers.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('teacher_id')
    )
    op.create_table('students',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('firstname', sa.String(), nullable=False),
    sa.Column('lastname', sa.String(), nullable=False),
    sa.Column('gender', sa.String(), nullable=False),
    sa.Column('phone_number', sa.String(), nullable=True),
    sa.Column('dob', sa.DateTime(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('learning_path', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('subject_teachers_class_id', sa.UUID(), nullable=True),
    sa.Column('teachers_class_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['subject_teachers_class_id'], ['subject_teachers_classes.id'], ),
    sa.ForeignKeyConstraint(['teachers_class_id'], ['teachers_classes.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('students')
    op.drop_table('teachers_classes')
    op.drop_table('subject_teachers_classes')
    op.drop_table('teachers')
    # ### end Alembic commands ###
