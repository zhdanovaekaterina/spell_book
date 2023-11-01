import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .models import Base
from src.core import config as c
from src.core.db.models import School

logger = logging.getLogger(__name__)


class DataBase:

    def __init__(self, url, registry):
        self.registry = registry
        self.engine = create_engine(url)

    def create_all(self):
        """
        Создание таблиц
        :return:
        """

        self.registry.metadata.create_all(self.engine)

    def get_tables_list(self):
        """
        Возвращает список таблиц в базе данных
        :return:
        """

        return self.registry.metadata.sorted_tables

    def add(self, entity: Base):

        with Session(self.engine) as session:
            with session.begin():
                session.add(entity)
            session.flush()

    def get(self, entity: Base, filter: dict):

        key = list(filter.keys())
        value = list(filter.values())

        with Session(self.engine) as session:
            return session.query(School).filter(getattr(entity, key[0]) == value[0]).one()

