"""02

Revision ID: ad51c05f6cb5
Revises: 6487840f47db
Create Date: 2023-11-13 22:25:42.689746

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'ad51c05f6cb5'
down_revision: Union[str, None] = '6487840f47db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('countrip_effect')
    op.drop_column('cast_type', 'learn_spells')
    op.drop_column('cast_type', 'prepare_spells')
    op.add_column('class', sa.Column('learn_spells', sa.Boolean(), nullable=False))
    op.add_column('class', sa.Column('prepare_spells', sa.Boolean(), nullable=False))
    op.add_column('spell_effect', sa.Column('add_dice_count', sa.SmallInteger(), nullable=True))
    op.add_column('spell_effect', sa.Column('damage_type_alias', sa.String(length=32), nullable=False))
    op.add_column('spell_effect', sa.Column('half_damage_on_success', sa.Boolean(), nullable=False))
    op.drop_constraint('spell_effect_ibfk_2', 'spell_effect', type_='foreignkey')
    op.create_foreign_key(None, 'spell_effect', 'damage_type', ['damage_type_alias'], ['alias'])
    op.drop_column('spell_effect', 'damage_type')
    op.drop_column('spell_effect', 'cell_level')
    op.add_column('spell_roll', sa.Column('characteristic', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('spell_roll', 'characteristic')
    op.add_column('spell_effect', sa.Column('cell_level', mysql.SMALLINT(), autoincrement=False, nullable=False))
    op.add_column('spell_effect', sa.Column('damage_type', mysql.VARCHAR(length=32), nullable=False))
    op.drop_constraint(None, 'spell_effect', type_='foreignkey')
    op.create_foreign_key('spell_effect_ibfk_2', 'spell_effect', 'damage_type', ['damage_type'], ['alias'])
    op.drop_column('spell_effect', 'half_damage_on_success')
    op.drop_column('spell_effect', 'damage_type_alias')
    op.drop_column('spell_effect', 'add_dice_count')
    op.drop_column('class', 'prepare_spells')
    op.drop_column('class', 'learn_spells')
    op.add_column('cast_type', sa.Column('prepare_spells', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
    op.add_column('cast_type', sa.Column('learn_spells', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
    op.create_table('countrip_effect',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('spell_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('caster_level', mysql.SMALLINT(), autoincrement=False, nullable=False),
    sa.Column('dice_count', mysql.SMALLINT(), autoincrement=False, nullable=False),
    sa.Column('dice', mysql.SMALLINT(), autoincrement=False, nullable=False),
    sa.Column('damage_type', mysql.VARCHAR(length=32), nullable=False),
    sa.ForeignKeyConstraint(['damage_type'], ['damage_type.alias'], name='countrip_effect_ibfk_2'),
    sa.ForeignKeyConstraint(['spell_id'], ['spell.id'], name='countrip_effect_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###