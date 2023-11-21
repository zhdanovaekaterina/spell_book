import logging

import pytest

from src.core.db.models import Base
from src.spell.effect import SpellEffectApi, CountripEffectApi, EffectDatabaseDriver
from ..config import TEST_DB
from .data import effects_data

logger = logging.getLogger(__name__)


# TODO: разобраться как вызывать одну фикстуру из другой и инициализировать БД один раз
def create_db():
    """
    Создает и наполняет in-memory базу данных для работы с эффектами
    """

    db = EffectDatabaseDriver(TEST_DB, Base)
    db.create_all()
    db.add_many(effects_data())

    return db


@pytest.fixture(scope='module')
def spell_api():
    """
    Возвращает созданный объект api эффектов заклинаний
    """

    db = create_db()
    yield SpellEffectApi(db)


@pytest.fixture(scope='module')
def countrip_api():
    """
    Возвращает созданный объект api эффектов заговоров
    """

    db = create_db()
    yield CountripEffectApi(db)
