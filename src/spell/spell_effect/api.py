from .db_driver import SpellEffectDatabaseDriver


class SpellEffectApi:
    """
    Апи для работы с эффектами заклинаний
    """

    def __init__(self, db: SpellEffectDatabaseDriver):
        self.db = db

    def get(self, spell_id: int, cell_level: int = 0):
        """
        Получение эффекта для выбранного заклинания и уровня ячейки.
        Если уровень не передан, возвращаются все доступные эффекты всех ячеек.
        :param spell_id:
        :param cell_level:
        :return:
        """

        raw = self.db.get_spell_effect(spell_id)

        spell_effect = {
            'effects': {
                raw.get('damage_type'): str(raw.get('dice_count')) + 'd' + str(raw.get('dice'))
            },
            'half_damage_on_success': raw.get('half_damage_on_success')
        }

        return spell_effect

    def add(self, spell_id: int, spell_effect: dict):
        """
        Добавление нового эффекта для заклинания
        :param spell_id:
        :param spell_effect:
        :return:
        """
        pass
    