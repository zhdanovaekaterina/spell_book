import logging

from sqlalchemy.exc import NoResultFound

from src.core.db.db_driver import DatabaseDriver
from src.core.db.models import SpellEffect


logger = logging.getLogger(__name__)


class SpellEffectDatabaseDriver(DatabaseDriver):
    """
    Драйвер для работы с запросами для получения эффектов заклинаний
    """

    def get_spell_effect(self, spell_id):
        """
        Получение эффектов заклинания по его ID
        :return:
        """

        with self.session:
            try:
                data = self.session.query(SpellEffect)\
                    .filter(SpellEffect.spell_id == spell_id)\
                    .one()
            except NoResultFound:
                return None

            return {
                'damage_type': data.damage_type.alias,
                'dice_count': data.dice_count,
                'dice': data.dice,
                'spell_level': data.spell.level,
                'add_dice_count': data.add_dice_count,
            }
