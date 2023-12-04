import logging

from .fixture import clean_db, import_data, dict_db
from .data import dict_data
from src.core.importer import Importer
from src.core.db.models import School, TimeToCast, Distance, Duration

logger = logging.getLogger(__name__)


def test_get_data(dict_db):
    """
    Тест получения всех данных сущности
    :return:
    """

    db_data = dict_db.get(School)
    needed_data = dict_data()

    assert len(db_data) == len(needed_data)

    for num, item in enumerate(db_data):
        assert item.alias == needed_data[num].alias
        assert item.title == needed_data[num].title


def test_add_one_item(clean_db):
    """
    Тест добавления одной записи без связей в таблицу
    :param clean_db:
    :return:
    """

    assert len(clean_db.get_tables_list()) > 0

    school = School(alias='transmutation', title='Преобразование')
    clean_db.add(school)

    # Получение списка значений
    added = clean_db.get(School)
    assert len(added) == 1
    assert isinstance(added[0], School)
    assert added[0].alias == 'transmutation'

    # Получение одного значения
    added = clean_db.get_one(School)
    assert isinstance(added, School)
    assert added.alias == 'transmutation'


def test_add_couple_items(clean_db):
    """
    Тест добавления нескольких значений в базу
    :param clean_db:
    :return:
    """

    assert len(clean_db.get_tables_list()) > 0

    school1 = School(alias='illusion', title='Иллюзия')
    school2 = School(alias='abjuration', title='Преграждение')
    clean_db.add_many([school1, school2])

    added = clean_db.get(School)
    assert len(added) == 2
    assert isinstance(added[0], School)
    assert added[0].alias == 'illusion'


def test_import_values_through_objects(clean_db):
    """
    Тест импорта из объектов
    :return:
    """

    importer = Importer(clean_db)
    importer.add(entity='school', alias='transmutation', title='Преобразование')
    importer.add(entity='school', alias='illusion', title='Иллюзия')
    importer.import_data()

    added = clean_db.get(School)
    assert len(added) == 2
    assert isinstance(added[0], School)
    assert added[0].alias == 'transmutation'


def test_import_values_from_files(import_data):
    """
    Тест импорта из файлов
    :param import_data:
    :return:
    """
    db, paths = import_data
    importer = Importer(db)

    for p in paths:
        importer.add_from_file(p)
    importer.import_data()

    # Проверяем что в базу добавились все значения из файлов импорта
    for inst in [School, TimeToCast, Distance, Duration]:
        added = db.get(inst)
        assert len(added) > 0
