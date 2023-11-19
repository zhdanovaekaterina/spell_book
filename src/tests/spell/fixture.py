import logging

import pytest

from src.core.db.models import Base
from src.spell.spell_effect.db_driver import SpellEffectDatabaseDriver
from ..config import TEST_DB
from .data import effects_data

logger = logging.getLogger(__name__)


@pytest.fixture()
def effects_db():
    """
    Возвращает in-memory базу данных, заполненную тестовыми данными для работы с
    эффектами заклинаний
    """

    db = SpellEffectDatabaseDriver(TEST_DB, Base)
    db.create_all()
    db.add_many(effects_data())
    yield db
