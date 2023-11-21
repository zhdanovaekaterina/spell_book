from ..const import COUNTRIP_LEVEL, MAX_CELL_LEVEL, MIN_CHARACTER_LEVEL, MAX_CHARACTER_LEVEL


class SpellError(Exception):
    """
    Пользовательские исключения в модуле заклинаний
    """

    COUNTRIP_LEVEL = 0

    @staticmethod
    def invalid_cell_level(level):
        """
        Исключение при некорректно переданном уровне ячейки
        """
        return SpellError(f'Invalid cell level provided: {level}; '
                          f'must be between {COUNTRIP_LEVEL} and {MAX_CELL_LEVEL}')

    @staticmethod
    def invalid_character_level(level):
        """
        Исключение при некорректно переданном уровне персонажа
        """
        return SpellError(f'Invalid character level provided: {level}; '
                          f'must be between {MIN_CHARACTER_LEVEL} and {MAX_CHARACTER_LEVEL}')

    @staticmethod
    def effect_not_found(spell_id):
        """
        Исключение когда не найден эффект для заклинания
        """
        return SpellError(f'Effect for spell ID {spell_id} not found')

    @staticmethod
    def higher_level(spell_id, spell_level, cell_level):
        """
        Исключение когда заклинание имеет более высокий уровень,
        чем запрашиваемая ячейка
        """
        return SpellError(f'This spell has higher base cell level; spell ID: {spell_id}, '
                          f'spell level: {spell_level}, you asked for level {cell_level}')

    @staticmethod
    def internal_error():
        """
        Непредвиденная ошибка
        """
        return SpellError('There was an unhandled internal error')

    @staticmethod
    def countrip_from_spell():
        """
        Исключение при попытке получения эффекта заговора от заклинания
        """
        return SpellError('You are trying to get countrip effect from spell')

    @staticmethod
    def spell_from_countrip():
        """
        Исключение при попытке получения эффекта заклинания от заговора
        """
        return SpellError('You are trying to get spell effect from countrip')
