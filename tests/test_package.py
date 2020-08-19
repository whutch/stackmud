# -*- coding: utf-8 -*-
"""Tests for the package itself."""
# Part of StackMUD (https://github.com/whutch/stackmud)
# :copyright: (c) 2020 Will Hutcheson
# :license: MIT (https://github.com/whutch/stackmud/blob/master/LICENSE.txt)

from stackmud import get_version


class TestPackage:

    """A collection of tests for the package."""

    def test_get_version(self):
        assert isinstance(get_version(), str)
