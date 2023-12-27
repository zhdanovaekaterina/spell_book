def parsed_list():
    return [
        {
            'link': 'https://dnd.su/spells/13-acid_splash/',
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


def params_for_detail_raw():
    return [
        (
            'tests/data/fake_countrip_detail.html',
            {
                'description': 'Описание заговора.\nВ нескольких абзацах.\nУрон этого заклинания увеличивается на 1к6, когда вы достигаете 5-го уровня (2к6), 11-го уровня (3к6) и 17-го уровня (4к6).\n',
                'classes': ['волшебник', 'чародей'],
                'subclasses': ['артиллерист (изобретатель)'],
                'time_to_cast_alias': '1 действие',
                'distance_alias': '60 футов',
                'duration_alias': 'Мгновенная',
                'source_alias': "«Player's handbook»",
            }
        )
    ]


def params_for_detail():
    return [
        (
            'tests/data/fake_countrip_detail.html',
            {
                'classes': ['wizard', 'sorcerer'],
                'subclasses': ['artificier-gunner'],
                'effect_progress': '1d6',
                'description': 'Описание заговора.\nВ нескольких абзацах.\nУрон этого заклинания увеличивается на 1к6, когда вы достигаете 5-го уровня (2к6), 11-го уровня (3к6) и 17-го уровня (4к6).\n',
                'time_to_cast_alias': 'action',
                'distance_alias': '60',
                'duration_alias': 'instant',
                'source_alias': 'PH',
            }
        ),
    ]
