from src.core.db.init import DatabaseDriver


class SpellEffectApi:
    """
    Апи для работы с эффектами заклинаний
    """

    def __init__(self, db: DatabaseDriver):
        self.db = db

    # @staticmethod
    def get(self, spell_id: int, cell_level: int = 0):
        """
        Получение эффекта для выбранного заклинания и уровня ячейки.
        Если уровень не передан, возвращаются все доступные эффекты всех ячеек.
        :param spell_id:
        :param cell_level:
        :return:
        """

        effect_raw = self.db.get_spell_effect(spell_id)
        return effect_raw

    # @staticmethod
    def add(self, spell_id: int, spell_effect: dict):
        """
        Добавление нового эффекта для заклинания
        :param spell_id:
        :param spell_effect:
        :return:
        """
        pass
    