from src.core.db.models import School


def import_data_data():
    """
    Данные для фикстуры import_data
    :return:
    """

    return {

        # Одно значение для одного словаря
        'one_value': [
            {
                'entity': 'school',
                'alias': 'transmutation',
                'title': 'Преобразование',
            }
        ],

        # Несколько значений для одного словаря
        'couple_values': [
            {
                'entity': 'time_to_cast',
                'alias': 'action',
                'title': 'Действие',
            },
            {
                'entity': 'time_to_cast',
                'alias': 'bonus_action',
                'title': 'Бонусное действие',
            },
        ],

        # Несколько значений для разных словарей
        'mixed_values': [
            {
                'entity': 'distance',
                'alias': 'self',
                'title': 'На себя',
                'value': 0,
            },
            {
                'entity': 'duration',
                'alias': 'at_once',
                'title': 'Мгновенное',
                'value': 0,
            },
        ]
    }


def dict_data():
    """
    Данные для фикстуры dict_db
    :return:
    """
    return [
        School(
            title='Вызов',
            alias='conjuration'
        ),
        School(
            title='Некромантия',
            alias='necromancy'
        ),
        School(
            title='Воплощение',
            alias='evocation'
        ),
    ]
