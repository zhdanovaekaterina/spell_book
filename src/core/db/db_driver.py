import logging
from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.core.db.models import Base


logger = logging.getLogger(__name__)


class DatabaseDriver:

    def __init__(self, url, registry):
        self.registry = registry
        self.engine = create_engine(url)
        self.session = Session(self.engine)

    def create_all(self):
        """
        Создание таблиц с предварительной очисткой схемы базы данных
        :return:
        """

        self.registry.metadata.drop_all(self.engine)
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
    def _get_select_query(self, entity: Base, add_filter: dict = None):
        """
        Получить объект запроса
        :return:
        """
        query = self.session.query(entity)

        if add_filter:
            key = list(add_filter.keys())
            value = list(add_filter.values())
            query = query.filter(getattr(entity, key[0]) == value[0])

        return query

    # TODO: заменить add_filter на kwargs
    def get(self, entity: Base | List[Base], add_filter: dict = None):
        """
        Возвращает выборку из базы
        :param entity:
        :param add_filter:
        :return:
        """

        with self.session:
            query = self._get_select_query(entity, add_filter)
            return query.all()

    def get_one(self, entity: Base, add_filter: dict = None):
        """
        Возвращает одно найденное значение из базы
        :param entity:
        :param add_filter:
        :return:
        """
        with self.session:
            query = self._get_select_query(entity, add_filter)
            return query.one()
