# -*- coding: utf-8 -*-
"""Logging configuration and support."""
# Part of StackMUD (https://github.com/whutch/stackmud)
# :copyright: (c) 2020 Will Hutcheson
# :license: MIT (https://github.com/whutch/stackmud/blob/master/LICENSE.txt)

from datetime import datetime
import logging
from logging.config import dictConfig
from os import makedirs, path
import re

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


@settings.register("LOG_TIME_FORMAT_CONSOLE")
class LogTimeFormatConsoleSetting(LogSetting):
    default = "%H:%M:%S,%F"


@settings.register("LOG_TIME_FORMAT_FILE")
class LogTimeFormatFileSetting(LogSetting):
    default = "%Y-%m-%d %a %H:%M:%S,%F"


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
    dictConfig({
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "file": {
                "()": LogFormatter,
                "format": "%(asctime)s  %(name)-12s  %(levelname)-8s %(message)s",
                "datefmt": settings.LOG_TIME_FORMAT_FILE,
            },
            "console": {
                "()": LogFormatter,
                "format": "%(asctime)s  %(name)-10s  %(levelname)-8s %(message)s",
                "datefmt": settings.LOG_TIME_FORMAT_CONSOLE,
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "console",
            },
            "file": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "level": "DEBUG",
                "formatter": "file",
                "filename": settings.LOG_PATH,
                "when": settings.LOG_ROTATE_WHEN,
                "interval": settings.LOG_ROTATE_INTERVAL,
                "utc": settings.LOG_UTC_TIMES,
            }
        },
        "root": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
        },
    })


class LogFormatter(logging.Formatter):
    """Custom formatter for our logging handlers."""

    def formatTime(self, record, datefmt=None):
        """Convert a LogRecord's creation time to a string.

        If `datefmt` is provided, it will be used to convert the time through
        datetime.strftime.  If not, it falls back to the formatTime method of
        logging.Formatter, which converts the time through time.strftime.

        This custom processing allows for the full range of formatting options
        provided by datetime.strftime as opposed to time.strftime.

        There is additional parsing done to allow for the %F argument to be
        converted to 3-digit zero-padded milliseconds, as an alternative to
        the %f argument's usual 6-digit microseconds (because frankly that's
        just too many digits).

        :param LogRecord record: The record to be formatted
        :param str datefmt: A formatting string to be passed to strftime
        :returns str: A formatted time string

        """
        if datefmt:
            msecs = str(int(record.msecs)).zfill(3)
            datefmt = re.sub(r"(?<!%)%F", msecs, datefmt)
            parsed_time = datetime.fromtimestamp(record.created)
            return parsed_time.strftime(datefmt)
        else:
            return super().formatTime(record)


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
