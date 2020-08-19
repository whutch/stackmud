# -*- coding: utf-8 -*-
"""Tests for the whole MUD process via a dummy client."""
# Part of StackMUD (https://github.com/whutch/stackmud)
# :copyright: (c) 2020 Will Hutcheson
# :license: MIT (https://github.com/whutch/stackmud/blob/master/LICENSE.txt)

from telnetlib import Telnet


class TestMeta:

    """A collection of tests for the whole MUD process."""

    client = Telnet()

    def test_meta(self):
        """Test several client interactions."""
