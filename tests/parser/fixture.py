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
