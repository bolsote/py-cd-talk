"""
This module provides a very simple implementation of feature flags, persisted
to a SQL database by default. The flags can be used by value or as decorators.
"""

from ensign._flags import (
    BinaryFlag,
    FlagDoesNotExist,
)
from ensign._storage import DefaultStorage


__all__ = (
    "BinaryFlag",
    "FlagDoesNotExist",
    "DefaultStorage",
)
