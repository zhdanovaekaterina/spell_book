import logging

from bs4 import BeautifulSoup
from aiohttp import ClientSession


logger = logging.getLogger(__name__)


class Parser:
    """
    Парсер заклинаний с dnd.su
    """

    def __init__(self):
        self.url = ''

    async def _get(self):
        """
        Отправляет GET-запрос
        """

        async with ClientSession() as session, session.get(self.url) as resp:
            return await resp.text()

    @staticmethod
    def _read_file(list_path):
        with open(list_path, 'r', encoding='utf-8') as file:
            return file.read()

    @staticmethod
    def _parse_list_data(soup_item):
        """
        Забирает данные заклинания из спискового представления
        :param soup_item:
        :return:
        """
        out = {
            'id': 0
        }
        return out

    def parse_list(self, list_path):
        """
        Забираем данные заклинаний из списка элементов в файле и парсит
        их данные в словарь
        :param list_path:
        :return:
        """
        raw_data = self._read_file(list_path)
        soup = BeautifulSoup(raw_data, 'html.parser')

        founded_items = soup.select('a')
        return [self._parse_list_data(item) for item in founded_items]
