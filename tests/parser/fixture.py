import os
import shutil
from pathlib import Path

import pytest

from src.parser.parser import Parser
from .mock import mock_get


@pytest.fixture()
def fake_parser(monkeypatch):
    """
    Отдает парсер с измененным методом get() для чтения данных из файла
    :return:
    """
    monkeypatch.setattr(Parser, "get", mock_get)
    return Parser()


@pytest.fixture(scope='module')
def temp_dir():
    """
    Создает директорию для хранения временных файлов и очищает ее после теста
    :return:
    """

    # Создать директорию для хранения временных файлов
    temp_dir_path = Path(Path.cwd(), 'tests', 'temp')
    if not os.path.isdir(temp_dir_path):
        os.mkdir(temp_dir_path)

    yield temp_dir_path

    # Очистить директорию с временными файлами
    shutil.rmtree(temp_dir_path)
