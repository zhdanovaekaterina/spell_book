import logging

from sqlalchemy.exc import NoResultFound

from src.core.db.db_driver import DatabaseDriver
from src.core.db.models import Effect
from src.core.error import SpellError


logger = logging.getLogger(__name__)


class EffectDatabaseDriver(DatabaseDriver):
    """
    Драйвер для работы с запросами для получения эффектов заклинаний
    """

    def get_effect(self, obj):
        """
        Получение эффектов сущности по ID и добавление атрибутов к объекту
        :return:
        """

        with self.session:
            try:
                data = self.session.query(Effect)\
                    .filter(Effect.spell_id == obj.spell_id)\
                    .one()
            except NoResultFound:
                raise SpellError.effect_not_found(obj.spell_id)

            obj.add(
                damage_type=data.damage_type.alias,
                dice_count=data.dice_count,
                dice=data.dice,
                spell_level=data.spell.level,
                add_dice_count=data.add_dice_count,
            )
