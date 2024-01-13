import sys
import csv

import src.helpers.helpers as helpers


class Importer:
    """
    Класс для импорта объектов в базу данных
    """

    MODELS_PATH = 'src.core.db.models'

    def __init__(self, db):

        self.collection = []
        self.db = db

    def add(self, **kwargs):
        """
        Добавление нового элемента
        :param kwargs:
        :return:
        """

        if not kwargs.get('entity'):
            raise AttributeError('Необходимо передать сущность')

        entity = kwargs['entity']
        del kwargs['entity']

        class_name = helpers.snake_to_camel(entity)
        obj = getattr(sys.modules[Importer.MODELS_PATH], class_name)
        new_entity = obj(**kwargs)

        self.collection.append(new_entity)

    def add_from_file(self, file_path):
        """
        Добавление новых элементов из файла csv
        :param file_path: Путь к файлу
        :return:
        """

        input_file = csv.DictReader(open(file_path))

        for row in input_file:
            self.add(**row)

    def import_data(self):
        """
        Импорт данных в базу данных
        :return:
        """

        self.db.add_many(self.collection)
