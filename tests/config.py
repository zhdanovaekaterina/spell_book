# Конфиг тестового окружения


import logging


logger = logging.getLogger(__name__)


# Настройки базы данных
TEST_DB = 'sqlite:///:memory:'


# Настройки логгирования
log_level = logging.INFO
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'
