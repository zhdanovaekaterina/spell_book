import logging
import re

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

        href = soup_item['href']

        spell_id = int(re.findall(r'\d+', href)[0])
        alias = href.split('-')[-1][:-1]

        title = soup_item.select('span.cards_list__item-name')[0].text
        level = int(soup_item.select('span.cards_list__item-prefix > span')[0].text)

        school_el_classes = soup_item.select('span.cards_list__item-icon > span')[0]['class']
        school_alias = school_el_classes[-1].split('_')[-1]

        components_alias_raw = soup_item.select('span.cards_list__item-suffix')[0].text
        components_alias = components_alias_raw.replace('В', 'v').replace('С', 's').replace('М', 'm').replace('.', '-')

        entity_alias = 'countrip' if level == 0 else 'spell'

        concentration = bool(soup_item.select('span.concentration'))
        ritual = bool(soup_item.select('span.ritual'))

        return {
            'link': 'https://dnd.su' + href,
            'id': spell_id,
            'alias': alias,
            'title': title,
            'level': level,
            'school_alias': school_alias,
            'components_alias': components_alias,
            'entity_alias': entity_alias,
            'concentration': concentration,
            'ritual': ritual,
            'is_active': True,
        }

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
