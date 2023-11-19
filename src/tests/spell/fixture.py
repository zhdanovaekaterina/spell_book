import logging

import pytest

from src.core.db.models import Base
from src.spell.spell_effect.db_driver import SpellEffectDatabaseDriver
from ..config import TEST_DB
from .data import effects_data
from src.spell.spell_effect.api import SpellEffectApi

logger = logging.getLogger(__name__)


@pytest.fixture(scope='module')
def api():
    """
    Создает и наполняет in-memory базу данных для работы с эффектами заклинаний
    Возвращает созданный объект api
    """

    db = SpellEffectDatabaseDriver(TEST_DB, Base)
    db.create_all()
    db.add_many(effects_data())
    api = SpellEffectApi(db)

    yield api
