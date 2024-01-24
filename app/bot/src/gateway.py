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
