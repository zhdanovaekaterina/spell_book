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
