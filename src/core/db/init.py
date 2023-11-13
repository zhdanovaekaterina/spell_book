import logging
from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .models import Base, SpellEffect
from src.core.db.models import School

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

    def get(self, entity: Base, add_filter: dict = None):
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

    # TODO: не нравится ОЧЕНЬ - подключение не должно использовать модели
    def get_spell_effect(self, spell_id):
        """
        Получение эффектов для выбранного заклинания и ячейки
        :return:
        """

        with self.session:
            query = self.session.query(SpellEffect)\
                .filter(SpellEffect.spell_id == spell_id)
            result = query.one()

            spell_effect = {
                'effects': {
                    result.damage_type.alias: str(result.dice_count) + 'd' + str(result.dice)
                },
                'half_damage_on_success': result.half_damage_on_success
            }

            return spell_effect
