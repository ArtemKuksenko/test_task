import functools
import os
import sys
import logging


class Logger:
    # формат сообщений
    DEFAULT_FORMAT = ('%(asctime)s %(levelname)s(%(filename)s:%(lineno)d): %(message)s', '%a, %d %b %Y %H:%M:%S')

    def __init__(self, name, level=logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # т.к. exception внутри себя вызывает error, то номер строки
        # и имя файла, в котором возникло исключение, определяется неверно,
        # поэтому необходимо создать proxy-метод, который решает эту "проблему"
        self.logger.exception = functools.partial(self.logger.error, exc_info=1)

        # Добавляем по умолчанию запись в файл
        log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../logs")
        self.add_file_rotate(os.path.join(log_path, "access.log"), level=level)
        self.add_file_rotate(os.path.join(log_path, "error.log"), level=logging.ERROR)

        # Добавляем по умолчанию запись в console
        self.add_console(level=level)

    def add_file_rotate(self, path, level=logging.DEBUG, mode='a+t', maxBytes=0, backupCount=0, encoding='utf-8'):
        """
        Добавляет файловый обработчик с ротацией файлов.
        path - путь к файлу, в который будет производиться запись
        mode - режим доступа при работе с файлом
        maxBytes - максимальный размер файла для ротации
        backupCount - количество старых файлов
        """
        from logging import handlers

        handler = handlers.RotatingFileHandler(path, mode=mode, maxBytes=maxBytes, backupCount=backupCount,
                                               encoding=encoding)
        return self.add_handler(handler, level)

    def add_console(self, level=logging.DEBUG):
        """
        Добавляет вывод на консоль.
        """
        self.add_stream(sys.stdout, level=level)

    def add_stream(self, stream, level=logging.DEBUG):
        """
        Добавляет потоковый обработчик записи сообщений.
        stream - поток, в который будет производиться запись
        """
        handler = logging.StreamHandler(stream)
        return self.add_handler(handler, level)

    def add_handler(self, handler, level):
        self.logger.addHandler(handler)

        handler.setLevel(level)
        handler.setFormatter(logging.Formatter(*Logger.DEFAULT_FORMAT))
        return handler

    def remove_handler(self, handler):
        """
        Удаляет ранее добавленный обработчик.
        """
        self.logger.removeHandler(handler)
