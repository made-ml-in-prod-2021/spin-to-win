import os
import logging
from logging import handlers

def setup_logger(logger_name, logger_path='./logfiles'):
    """ Создает логгер

    1. печатает в stdout сообщения класса debug, info и warning 
    2. пишет лог файл со всеми сообщениями в лог файл


    :logger_name:
    название логгера. Будет стоять в названиях лог-файлов.

    :logger_path:
    директория для лог-файлов. Создает новую директорию, если указанной не существует


    *** Как пользоваться ***
    # инициализировать: logger = setup_logger(...)
    # заменить все 'print' на 'logger.info' 
    # вместо info также есть уровни: debug, warning, error, critical 

    *** Полезно знать ***
    # print умеет принимать несколько аргументов: print(a, b, c), но logger так не умеет!
    # поэтому можно через f-стринги:  logger.info(f'{a} {b} {c}')
    # либо через %s:  logger.info('%s %s!', 'Hello', 'world')

    """

    if not os.path.exists(logger_path):
        os.makedirs(logger_path)

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    FORMAT = '%(asctime)s # %(lineno)04d # %(levelname)s # %(message)s'
    fmt = logging.Formatter(FORMAT, datefmt='%Y-%m-%d %H:%M:%S')

    # clear previous handlers if exists 
    logger.handlers.clear()

    class LevelFilter():
        def __init__(self, low, high):
            self._low = low
            self._high = high
        def filter(self, record):
            return bool(self._low <= record.levelno <= self._high)

    # console hahdler (only debug, info and warning messages)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(fmt)
    ch.addFilter(LevelFilter(10, 30))   # debug + info + warning
    logger.addHandler(ch)

    # full log with all tracebacks & all history
    file_name1 = os.path.join(logger_path, logger_name + '.log')
    rotate_handler = logging.FileHandler(file_name1)
    rotate_handler.setLevel(logging.DEBUG)
    rotate_handler.setFormatter(fmt)
    logger.addHandler(rotate_handler)

    return logger


