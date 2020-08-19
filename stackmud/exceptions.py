# -*- coding: utf-8 -*-
"""Custom exceptions."""
# Part of StackMUD (https://github.com/whutch/stackmud)
# :copyright: (c) 2020 Will Hutcheson
# :license: MIT (https://github.com/whutch/stackmud/blob/master/LICENSE.txt)


class AlreadyExists(Exception):
    """Exception for adding an item to a collection it is already in."""

    def __init__(self, key, old, new=None):
        self.key = key
        self.old = old
        self.new = new
