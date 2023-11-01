import logging

from .fixture import database
from src.core.db.models import School

logger = logging.getLogger(__name__)


def test_add_one_simple_item(database):
    """
    Тест добавления одной записи без связей в таблицу
    :param database:
    :return:
    """

    assert len(database.get_tables_list()) > 0

    school = School(alias='transmutation', title='Преобразование')
    database.add(school)

    added = database.get(School, {'alias': 'transmutation'})

    assert isinstance(added, School)
    assert added.alias == 'transmutation'

