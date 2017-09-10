"""
Feature flag-related classes. Provides an abstract flag implementation, and a
concrete implementation of a binary flag.
"""

import abc
import datetime
import enum

from functools import wraps
from zope.interface import implementer

from ensign._interfaces import IFlag
from ensign._storage import DefaultStorage, FlagTypes


class FlagDoesNotExist(Exception):
    """
    Exception raised when trying to instantiate an inexisting flag.
    """


class FlagActive(enum.Enum):
    """
    Possible values for a flag activity indicator:
     - Inactive: Flag has not been used in DAYS_INACTIVE (see Flag class).
     - Active: Flag has been used recently.
     - New: Flag has never been used.
    """

    INACTIVE = 0
    ACTIVE = 1
    NEW = 2


class Flag(metaclass=abc.ABCMeta):
    """
    Flag base class, for all concrete flag implementations to inherit from.
    """

    TYPE = None
    DAYS_INACTIVE = 7

    def __init__(self, name, store=DefaultStorage):
        self.name = name
        self.store = store
        if not self.store.exists(self.name):
            raise FlagDoesNotExist()

    @classmethod
    def create(cls, name, store=DefaultStorage, **kwargs):
        """
        Create a new flag, given its name and extra arguments, in the provided
        store.
        """

        store.create(name, cls.TYPE, **kwargs)
        return cls(name, store=store)

    @classmethod
    def all(cls, store=DefaultStorage):
        """
        Return all flags in the store.
        """

        return [
            cls(flag, store=store)
            for flag in store.all()
        ]

    def __str__(self):
        return f"<Flag({self.name}={self.value})>"

    def __bool__(self):
        return self._check()

    def __and__(self, other):
        # pylint: disable=protected-access
        return self._check() & other._check()

    def __or__(self, other):
        # pylint: disable=protected-access
        return self._check() | other._check()

    def __xor__(self, other):
        # pylint: disable=protected-access
        return self._check() ^ other._check()

    def __invert__(self):
        return not self._check()

    def __call__(self, target):
        @wraps(target)
        def wrapper(*args, **kwargs):
            """
            If the flag evaluates to True, go through with the target
            function. Otherwise, skip it.
            """

            if self._check():
                return target(*args, **kwargs)

        return wrapper

    @abc.abstractmethod
    def _check(self):
        """
        Returns the result of evaluating the flag. Must be a boolean value.
        """

    @property
    def value(self):
        """
        Get the flag's stored value.
        """

        return self.store.load(self.name, self.TYPE)

    @value.setter
    def value(self, val):
        """
        Set the flag's stored value.
        """

        self.store.store(self.name, val, self.TYPE)

    @property
    def active(self):
        """
        Return the flag's activity indicator. See the FlagActive's enum.
        """

        used = self.store.used(self.name)
        if used is None:
            return FlagActive.NEW

        diff = datetime.datetime.now() - used
        if diff > datetime.timedelta(days=7):
            return FlagActive.INACTIVE

        return FlagActive.ACTIVE

    @property
    def info(self):
        """
        Return the flag's descriptive information. To be used in user-facing
        interfaces.
        """

        info = self.store.info(self.name)
        return dict(
            name=info["name"],
            label=info["label"] or "",
            description=info["description"] or "",
            tags=info["tags"] or "",
        )


@implementer(IFlag)
class BinaryFlag(Flag):
    """
    Implementation of a flag storing a boolean value.
    """

    TYPE = FlagTypes.BINARY

    def _check(self):
        return self.value

    def set(self):
        """
        Shortcut method to set() (to True) the flag's value.
        """

        self.value = True

    def unset(self):
        """
        Shortcut method to unset() (to False) the flag's value.
        """

        self.value = False
