"""First migrations

Revision ID: e15300b814dd
Revises: 
Create Date: 2024-07-04 23:05:34.815618

"""
from alembic import op
import sqlalchemy as sa


revision = 'e15300b814dd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('charityproject',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('full_amount', sa.Integer(), nullable=False, comment='Требуемая сумма, целочисленное поле; больше 0;'),
    sa.Column('invested_amount', sa.Integer(), nullable=True, comment='Внесённая сумма, целочисленное поле; значение по умолчанию — 0;'),
    sa.Column('fully_invested', sa.Boolean(), nullable=True, comment='Булево значение, указывающее на то, собрана ли нужная сумма (закрыт ли проект); значение по умолчанию — False;'),
    sa.Column('create_date', sa.DateTime(), nullable=True, comment='дата пожертвования; тип DateTime; добавляется автоматически в момент поступления пожертвования;'),
    sa.Column('close_date', sa.DateTime(), nullable=True, comment='дата, когда вся сумма пожертвований была распределена по проектам; тип DateTime; добавляется автоматически в момент выполнения условия.'),
    sa.Column('name', sa.String(length=100), nullable=False, comment='Уникальное название проекта, обязательное строковое поле; допустимая длина строки — от 1 до 100 символов включительно;'),
    sa.Column('description', sa.String(), nullable=False, comment='Описание, обязательное поле, текст; не менее одного символа;'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=320), nullable=False),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_table('donation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('full_amount', sa.Integer(), nullable=False, comment='Требуемая сумма, целочисленное поле; больше 0;'),
    sa.Column('invested_amount', sa.Integer(), nullable=True, comment='Внесённая сумма, целочисленное поле; значение по умолчанию — 0;'),
    sa.Column('fully_invested', sa.Boolean(), nullable=True, comment='Булево значение, указывающее на то, собрана ли нужная сумма (закрыт ли проект); значение по умолчанию — False;'),
    sa.Column('create_date', sa.DateTime(), nullable=True, comment='дата пожертвования; тип DateTime; добавляется автоматически в момент поступления пожертвования;'),
    sa.Column('close_date', sa.DateTime(), nullable=True, comment='дата, когда вся сумма пожертвований была распределена по проектам; тип DateTime; добавляется автоматически в момент выполнения условия.'),
    sa.Column('user_id', sa.Integer(), nullable=True, comment='id пользователя, сделавшего пожертвование. Foreign Key на поле user.id из таблицы пользователей;'),
    sa.Column('comment', sa.String(), nullable=True, comment='Комментарий, необязательное текстовое поле;'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='donation_id_user'),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('donation')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('charityproject')
