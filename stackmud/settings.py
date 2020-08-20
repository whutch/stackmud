# -*- coding: utf-8 -*-
"""Setting registration and management."""
# Part of StackMUD (https://github.com/whutch/stackmud)
# :copyright: (c) 2020 Will Hutcheson
# :license: MIT (https://github.com/whutch/stackmud/blob/master/LICENSE.txt)

from .utils import Manager


class Unset:
    """A sentinel value that we can distinguish from None."""


class Setting:

    default = Unset  # This should NOT be a mutable value.
    read_only = False
    read_only_once_set = False

    def __init__(self, name):
        self._name = name
        self._value = Unset
        self._do_lazy_update = True
        self.value = self.default

    @property
    def value(self):
        if self._do_lazy_update:
            self._do_lazy_update = False
            self.lazy_update()
        return self._value

    @value.setter
    def value(self, value):
        if self.read_only:
            raise ValueError(f"setting '{self._name}' is read-only")
        if self.read_only_once_set and \
                (self._value is self.default or self._value == self.default):
            raise ValueError(f"setting '{self._name}' is read-only")
        self.validate(value)
        if (value is self._value or value == self._value):
            return
        self._value = value
        self.update()
        self._do_lazy_update = True

    def validate(self, value):
        pass

    def update(self):
        pass

    def lazy_update(self):
        pass


class SettingManager(Manager):

    _managed_type = Setting
    _instances = True

    def __getattr__(self, name):
        if name.startswith("_"):
            return super().__getattribute__(name)
        if name not in self._items:
            raise AttributeError(f"no setting '{name}'")
        return self._items[name].value

    def __setattr__(self, name, value):
        if name.startswith("_"):
            return super().__setattr__(name, value)
        if name not in self._items:
            raise AttributeError(f"no setting '{name}'")
        setting = self._items[name]
        setting.value = value

    def register(self, name):
        _decorator = super().register(name)

        def decorator(setting_class):
            instance = setting_class(name)
            return _decorator(instance)

        return decorator


# Global settings for the whole package.
settings = SettingManager()
