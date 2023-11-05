import logging

import pytest

from src.core.db.init import DataBase
from src.core.db.models import Base

from ..config import TEST_DB

logger = logging.getLogger(__name__)


@pytest.fixture()
def clean_db():
    """
    Возвращает пустую in-memory базу данных
    """

    db = DataBase(TEST_DB, Base)
    db.create_all()

    yield db
