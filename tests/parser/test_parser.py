from src.parser.parser import Parser


result = [
    {
        'id': 13,
        'alias': 'acid_splash',
        'title': 'Брызги кислоты',
        'level': 0,
        'school_alias': 'conjuration',
        'components_alias': 'vs-',
        'entity_alias': 'countrip',
        'concentration': False,
        'ritual': False,
        'is_active': True,
    },
]


def test_parse_spell_list():
    """
    Тест парсинга данных заклинаний из списка
    :return:
    """
    parser = Parser()
    spell_list = parser.parse_list('tests/parser/fake_spell_list.html')
    print(spell_list)
