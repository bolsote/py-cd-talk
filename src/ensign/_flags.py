import abc
import datetime
import enum

from functools import wraps
from zope.interface import implementer

from ensign._interfaces import IFlag
from ensign._storage import DefaultStorage, FlagTypes


class FlagActive(enum.Enum):
    INACTIVE = 0
    ACTIVE = 1
    NEW = 2


class Flag(metaclass=abc.ABCMeta):
    TYPE = None
    DAYS_INACTIVE = 7

    def __init__(self, name, store=DefaultStorage, **kwargs):
        self.name = name
        self.store = store
        self.store.create(self.name, self.TYPE, **kwargs)

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
            if self._check():
                return target(*args, **kwargs)
        return wrapper

    @abc.abstractmethod
    def _check(self):
        return False

    @property
    def value(self):
        return self.store.load(self.name)

    @value.setter
    def value(self, val):
        self.store.store(self.name, val)

    @property
    def active(self):
        used = self.store.used(self.name)
        if used is None:
            return FlagActive.NEW

        diff = datetime.datetime.now() - used
        if diff > datetime.timedelta(days=7):
            return FlagActive.INACTIVE

        return FlagActive.ACTIVE


@implementer(IFlag)
class BinaryFlag(Flag):
    TYPE = FlagTypes.BINARY

    def _check(self):
        return self.value

    def set(self):
        self.value = True

    def unset(self):
        self.value = False
