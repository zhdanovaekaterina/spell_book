import csv


class FileHelper:
    """
    Набор методов для работы с файлами
    """

    @staticmethod
    def read_file(list_path):
        """
        Чтение данных из файла
        :param list_path:
        :return:
        """

        with open(list_path, 'r', encoding='utf-8') as file:
            return file.read()

    @staticmethod
    def to_csv(data: dict, path, mode='w'):
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
    def read_csv(list_path):
        """
        Чтение данных из файла
        :param list_path:
        :return:
        """

        with open(list_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return [row for row in reader]
        