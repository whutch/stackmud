# -*- coding: utf-8 -*-
"""Logging configuration and support."""
# Part of StackMUD (https://github.com/whutch/stackmud)
# :copyright: (c) 2022 Will Hutcheson
# :license: MIT (https://github.com/whutch/stackmud/blob/master/LICENSE.txt)

import logging
from logging.handlers import TimedRotatingFileHandler
from os import makedirs, path

from .settings import Setting, settings


logging_config_dirty = True


class LogSetting(Setting):

    def update(self):
        global logging_config_dirty
        logging_config_dirty = True


@settings.register("LOG_PATH")
class LogPathSetting(LogSetting):
    default = path.join(".", "logs", "mud.log")

    def lazy_update(self):
        parent_dir = path.dirname(self._value)
        if not path.exists(parent_dir):
            makedirs(parent_dir)


@settings.register("LOG_MESSAGE_FORMAT_CONSOLE")
class LogMessageFormatConsoleSetting(LogSetting):
    default = "%(asctime)s.%(msecs)03d  %(name)-12s  %(levelname)-8s %(message)s"


@settings.register("LOG_TIME_FORMAT_CONSOLE")
class LogTimeFormatConsoleSetting(LogSetting):
    default = "%H:%M:%S"


@settings.register("LOG_MESSAGE_FORMAT_FILE")
class LogMessageFormatFileSetting(LogSetting):
    default = "%(asctime)s.%(msecs)03d  %(name)-12s  %(levelname)-8s %(message)s"


@settings.register("LOG_TIME_FORMAT_FILE")
class LogTimeFormatFileSetting(LogSetting):
    default = "%Y-%m-%d %a %H:%M:%S"


@settings.register("LOG_ROTATE_WHEN")
class LogRotateWhenSetting(LogSetting):
    default = "midnight"


@settings.register("LOG_ROTATE_INTERVAL")
class LogRotateIntervalSetting(LogSetting):
    default = 1


@settings.register("LOG_UTC_TIMES")
class LogUTCTimesSetting(LogSetting):
    default = False


def update_logging_config():
    # Remove any existing handlers
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        root_logger.removeHandler(handler)
    # Create the console handler
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(
        fmt=settings.LOG_MESSAGE_FORMAT_CONSOLE,
        datefmt=settings.LOG_TIME_FORMAT_CONSOLE,
    )
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    # Create the file handler
    file_handler = TimedRotatingFileHandler(
        settings.LOG_PATH,
        when=settings.LOG_ROTATE_WHEN,
        interval=settings.LOG_ROTATE_INTERVAL,
        backupCount=0,
        delay=True,
        utc=settings.LOG_UTC_TIMES,
        atTime=None,
    )
    file_formatter = logging.Formatter(
        fmt=settings.LOG_MESSAGE_FORMAT_FILE,
        datefmt=settings.LOG_TIME_FORMAT_FILE,
    )
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)
    # Set the default level for all handlers
    root_logger.setLevel(logging.DEBUG)


def get_logger(*args, **kwargs):
    """Fetch an instance of logging.Logger.

    This is just a stub that can later be expanded if we want to perform any
    processing on the Logger instance before passing it on.

    Using this as a middle-man also ensures that our logging configuration will
    always be loaded before a Logger is used, as none of the other code will
    load the logging module directly.

    :param sequence args: Positional arguments passed on to logging.getLogger
    :param mapping kwargs: Keyword arguments passed on to logging.getLogger
    :returns logging.Logger: A Logger instance

    """
    global logging_config_dirty
    if logging_config_dirty:
        update_logging_config()
        logging_config_dirty = False
    logger = logging.getLogger(*args, **kwargs)
    return logger
