# import os
from collections import namedtuple

import pytest

import sqlalchemy as sa
from zope.interface import implementer

from ensign import BinaryFlag
from ensign._interfaces import IStorage
from ensign._storage import DefaultStorage


STORE = {}


@implementer(IStorage)
class FakeStorage:
    STORE = {}

    def create(self, name, type, **kwargs):
        self.STORE[name] = dict(
            name=name,
            type=type,
            value_binary=None,
            **kwargs,
        )

    def load(self, name):
        return self.STORE[name]["value_binary"]

    def store(self, name, value):
        self.STORE[name]["value_binary"] = value


@pytest.fixture(scope="function")
def fakestore():
    return FakeStorage()


@pytest.fixture(scope="function")
def fakeflag(fakestore):
    return BinaryFlag("fakeflag", store=fakestore)


@pytest.fixture(scope="session")
def _pre_db():
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
    conn = DefaultStorage.connection
    trans = conn.begin()
    yield
    trans.rollback()
