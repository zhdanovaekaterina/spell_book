import logging
from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .models import Base
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
        """
        Добавляет одно значение в базу
        :param entity:
        :return:
        """

        with Session(self.engine) as session:
            with session.begin():
                session.add(entity)

    def add_many(self, entity_list: List[Base]):
        """
        Добавляет несколько значений в базу
        :param entity_list:
        :return:
        """

        with Session(self.engine) as session:
            with session.begin():
                session.bulk_save_objects(entity_list)

    # TODO: добавить обработку фильтра с несколькими условиями
    def get(self, entity: Base, add_filter: dict = None):
        """
        Возвращает выборку из базы
        :param entity:
        :param add_filter:
        :return:
        """

        with Session(self.engine) as session:
            query = session.query(entity)

            if add_filter:
                key = list(add_filter.keys())
                value = list(add_filter.values())
                query = query.filter(getattr(entity, key[0]) == value[0])

            return query.all()
