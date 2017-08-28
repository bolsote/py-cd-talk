# pylint: skip-file

from zope.interface import Attribute, Interface


class IFlag(Interface):
    """
    Flag Interface.

    Any kind of flag must implement this interface.
    """

    TYPE = Attribute("""Flag type""")
    store = Attribute("""Flag storage backend""")
    name = Attribute("""Flag name""")
    value = Attribute("""Flag value""")

    def _check():
        """
        Check whether the flag current value means the feature is active.
        """


class IStorage(Interface):
    """
    Storage Interface.

    Any kind of backing storage for flags must implement this interface.
    """

    def create(name, type, **kwargs):
        """Create a new flag."""

    def load(name):
        """Load a value."""

    def store(name, value):
        """Store a value."""
