# -*- coding: utf-8 -*-
"""The main entry point for this package."""
# Part of StackMUD (https://github.com/whutch/stackmud)
# :copyright: (c) 2022 Will Hutcheson
# :license: MIT (https://github.com/whutch/stackmud/blob/master/LICENSE.txt)

from . import get_version
from .logs import get_logger


logger = get_logger("main")


if __name__ == "__main__":
    logger.info(f"StackMUD {get_version()}")
