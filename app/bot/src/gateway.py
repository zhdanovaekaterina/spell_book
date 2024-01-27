class Gateway:
    """
    Шлюз обмена данными с ядром
    """

    @staticmethod
    def get_classes():
        """
        Получение словаря классов, добавленных в систему
        """

        return {
            'bard': 'Бард',
            'wizard': 'Волшебник',
            'cleric': 'Жрец',
        }

    @staticmethod
    def get_available_actions(user_class):
        """
        Получение доступных действий для класса
        """

        match user_class:
            case 'bard':
                return {
                    'learn': True,
                    'prepare': False,
                }
            case 'wizard':
                return {
                    'learn': True,
                    'prepare': True,
                }
            case 'cleric':
                return {
                    'learn': False,
                    'prepare': True,
                }

    @staticmethod
    def register_user(user_class, user_level):
        """
        Регистрация кастера определенного класса и уровня.
        Возвращает id кастера в системе
        """

        return 1

    @staticmethod
    def check_valid_level(level) -> bool:
        """
        Проверяет, является ли переданное значение
        корректным уровнем персонажа (числом от 1 до 20)
        """

        try:
            passed_level = int(level)
            return 1 <= passed_level <= 20

        except ValueError:
            return False

    @staticmethod
    def spell_list_available(user_id):
        """
        Получение списка доступных заклинаний для кастера
        """
        return fake_spell_list()

    @staticmethod
    def spell_list_learned(user_id):
        """
        Получение списка изученных заклинаний для кастера
        """
        return fake_spell_list()

    @staticmethod
    def spell_list_prepared(user_id):
        """
        Получение списка подготовленных заклинаний для кастера
        """
        return fake_spell_list()


def fake_spell_list():
    return [
        {
            'alias': 'spell_1',
            'title': 'Заклинание 1',
            'level': 1
        },
        {
            'alias': 'spell_2',
            'title': 'Заклинание 2',
            'level': 1
        },
        {
            'alias': 'spell_3',
            'title': 'Заклинание 3',
            'level': 1
        },
        {
            'alias': 'spell_4',
            'title': 'Заклинание 4',
            'level': 1
        },
    ]
