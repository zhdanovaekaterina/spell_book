import logging
import re
import csv
from time import sleep

from bs4 import BeautifulSoup
from aiohttp import ClientSession


logger = logging.getLogger(__name__)


class Parser:
    """
    Парсер заклинаний с dnd.su
    """

    LIMIT = 20  # Размер партии, которую будем парсить за один раз
    TIMEOUT = 3  # Таймаут запросов

    def __init__(self):
        self.url = ''
        self.dictionaries = []

    async def get(self, url):
        """
        Отправляет GET-запрос
        """

        async with ClientSession() as session, session.get(url) as resp:
            return await resp.text()

    @staticmethod
    def _read_file(list_path):
        """
        Чтение данных из файла
        :param list_path:
        :return:
        """

        with open(list_path, 'r', encoding='utf-8') as file:
            return file.read()

    @staticmethod
    def _to_csv(data, path, mode='w'):
        """
        Сохранение данных в csv
        :param data:
        :param path:
        :return:
        """

        keys = data[0].keys()

        with open(path, mode, newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)

    @staticmethod
    def _read_csv(list_path):
        """
        Чтение данных из файла
        :param list_path:
        :return:
        """

        with open(list_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return [row for row in reader]

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

    @staticmethod
    def _parse_detail_items(soup_item):
        """
        Забирает данные заклинания с детальной страницы
        :param soup_item:
        :return:
        """

        params = soup_item.select('.params > li')

        temp = {}
        for p in params:
            text = p.get_text()
            text_list = text.split(': ')

            if len(text_list) == 2:
                temp[text_list[0]] = text_list[1]

        description_raw = soup_item.select('div[itemprop="description"]')[0].get_text()
        description = description_raw.replace('\n', ' ')

        return {
            'description': description,
            'classes': temp.get('Классы'),
            'subclasses': temp.get('Архетипы'),
            'time_to_cast_alias': temp.get('Время накладывания'),
            'distance_alias': temp.get('Дистанция'),
            'duration_alias': temp.get('Длительность'),
            'source_alias': temp.get('Источник'),
        }

    async def parse_detail_raw(self, item_url):
        """
        Забираем данные заклинания по переданной ссылке с детальной страницы
        :param item_url:
        :return:
        """
        raw_data = await self.get(item_url)
        soup = BeautifulSoup(raw_data, 'html.parser')

        return self._parse_detail_items(soup)

    async def parse(self, list_path, target_path):
        """
        Парсинг всех данных заклинаний
        :param list_path: Путь, по которому лежит список всех заклинаний в html
        :param target_path: Путь, по которому необходимо сохранить файл с данными
        :return:
        """

        data = self.parse_list(list_path)

        offset = 0
        count = len(data)

        while offset < count:

            start = offset
            end = offset + self.LIMIT
            batch = data[start:end]

            logger.info(f'batch {start} - {end}')

            out = []
            for row in batch:
                parsed = await self.parse_detail_raw(row['link'])
                out.append(row | parsed)

            self._to_csv(out, target_path, 'a')
            offset += self.LIMIT

            sleep(self.TIMEOUT)
