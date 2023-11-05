import logging
import csv
import os
import shutil
from pathlib import Path

import pytest

from src.core.db.init import DataBase
from src.core.db.models import Base
from .data import import_data_data

from ..config import TEST_DB

logger = logging.getLogger(__name__)


def write_csv(file_name, file_data, temp_dir_path):
    """
    Пишет содержимое словаря file_data в файл csv с именем file_name во временной директории temp_dir_path.
    Возвращает путь к записанному файлу
    :return:
    """

    keys = file_data[0].keys()
    path = Path(temp_dir_path, f'{file_name}.csv')

    with open(path, 'w', newline='') as out:
        writer = csv.DictWriter(out, keys)
        writer.writeheader()
        writer.writerows(file_data)

    return path


@pytest.fixture()
def clean_db():
    """
    Возвращает пустую in-memory базу данных
    """

    db = DataBase(TEST_DB, Base)
    db.create_all()

    yield db


@pytest.fixture()
def import_data():
    """
    Возвращает пустую in-memory базу данных и пути к файлам для импорта.
    После завершения теста очищает директорию с временными файлами.
    """

    db = DataBase(TEST_DB, Base)
    db.create_all()

    # Создать директорию для хранения временных файлов
    temp_dir_path = Path(Path.cwd(), 'src', 'tests', 'temp')
    if not os.path.isdir(temp_dir_path):
        os.mkdir(temp_dir_path)

    # Импортировать тестовые данные
    data = import_data_data()
    paths = []

    # Записать данные в разные файлы и собрать пути файлов в список
    for file_name, file_data in data.items():
        path = write_csv(file_name, file_data, temp_dir_path)
        paths.append(path)

    yield db, paths

    # Очистить директорию с временными файлами
    shutil.rmtree(temp_dir_path)
