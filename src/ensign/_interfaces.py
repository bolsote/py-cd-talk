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
    active = Attribute("""Flag activity indicator""")
    info = Attribute("""Flag descriptive information""")

    def create(name, store, **kwargs):
        """
        Create a new flag with the given name and, optionally, extra data,
        persisted in the given store.
        """

    def all(store):
        """
        Retrieve all flags in the store.
        """

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

    def exists(name):
        """Check if the flag exists in the store."""

    def load(name, type):
        """Load a value."""

    def store(name, value, type):
        """Store a value."""

    def used(name):
        """Get last used date."""

    def info(name):
        """Get flag descriptive information."""

    def all():
        """Get all flags."""
