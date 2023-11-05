import logging

from .fixture import clean_db
from src.core.db.models import School

logger = logging.getLogger(__name__)


def test_add_one_item(clean_db):
    """
    Тест добавления одной записи без связей в таблицу
    :param clean_db:
    :return:
    """

    assert len(clean_db.get_tables_list()) > 0

    school = School(alias='transmutation', title='Преобразование')
    clean_db.add(school)

    added = clean_db.get(School)
    assert len(added) == 1
    assert isinstance(added[0], School)
    assert added[0].alias == 'transmutation'


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
