import logging

from sqlalchemy import create_engine

from models import Base
from core import config as c

logger = logging.getLogger(__name__)


class DataBase:

    def __init__(self):
        self.engine = create_engine(f"mysql+mysqlconnector://{c.MYSQL_USER}:{c.MYSQL_PASSWORD}"
                                    f"@{c.MYSQL_HOST}:{c.MYSQL_PORT}/{c.MYSQL_DATABASE}")

    def create_all(self):
        """
        Создание таблиц
        :return:
        """

        Base.metadata.create_all(self.engine)


if __name__ == '__main__':
    db = DataBase()
    db.create_all()
