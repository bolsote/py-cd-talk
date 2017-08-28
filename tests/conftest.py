"""
Test fixtures and test utilities.
"""

# pylint: disable=invalid-name,no-self-use,redefined-outer-name

import os

import pytest

import sqlalchemy as sa
from zope.interface import implementer
from zope.interface.verify import verifyObject

from ensign import BinaryFlag
from ensign._interfaces import IStorage
from ensign._storage import DefaultStorage


@implementer(IStorage)
class FakeStorage:
    """
    Fake storage class, to simulate a very simple datastore.
    """

    STORE = {}

    def __init__(self):
        assert verifyObject(IStorage, self)

    def create(self, name, flagtype, **kwargs):
        """
        Create a new flag, with its value set to None.
        """

        self.STORE[name] = dict(
            name=name,
            type=flagtype,
            value_binary=None,
            **kwargs,
        )

    def exists(self, name):
        return name in self.STORE

    def load(self, name):
        """
        Load a flag's value from the store, given its name.
        """

        return self.STORE[name]["value_binary"]

    def store(self, name, value):
        """
        Store a flag's value to the store, given its name.
        """

        self.STORE[name]["value_binary"] = value

    def used(self, name):
        """
        Get a flag's last used datetime, given its name.
        """

        return self.STORE[name].get("used")


@pytest.fixture(scope="function")
def fakestore():
    """
    Fixture providing a fake storage.
    It's cleaned up for every test.
    """

    return FakeStorage()


@pytest.fixture(scope="function")
def fakeflag(fakestore):
    """
    Fixture providing a flag stored in fake storage.
    It's generated anew for every test.
    """

    return BinaryFlag.create("fakeflag", store=fakestore)


@pytest.fixture(scope="session")
def _pre_db():
    """
    Fixture preparing the test database and establishing all the necessary
    connections, and cleaning everything up when done.
    The operations are performed just once per session.
    """

    engine = sa.create_engine(os.environ.get("MGMT_DB"))
    conn = engine.connect()
    conn.execute("commit")
    conn.execute("create database flags_test")
    DefaultStorage.init_db()
    yield
    DefaultStorage.connection.close()
    DefaultStorage.engine.dispose()
    conn.execute("commit")
    conn.execute("drop database flags_test")
    conn.close()
    engine.dispose()


@pytest.fixture(scope="function")
def db(_pre_db):
    """
    Fixture providing access to a test database.
    Transactions are rolled back for every test.
    """

    conn = DefaultStorage.connection
    trans = conn.begin()
    yield
    trans.rollback()
