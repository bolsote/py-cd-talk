"""
Storage-related classes. Provides a default storage, backed by a SQL database.
"""
# pylint: disable=invalid-name,no-value-for-parameter

import enum
import os

import sqlalchemy as sa
from zope.interface import implementer

from ensign._interfaces import IStorage


class FlagTypes(enum.Enum):
    """
    Enumeration with all the possible flag types available.
    """

    BINARY = "binary"


@implementer(IStorage)
class SQLStorage:
    """
    SQL-backed flag storage.
    """

    engine = None
    connection = None
    metadata = sa.MetaData()

    flags = sa.Table(
        "flags", metadata,
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.Unicode(64), nullable=False, unique=True),
        sa.Column("type", sa.Enum(FlagTypes), nullable=False),

        sa.Column("value_binary", sa.Boolean),

        sa.Column("label", sa.Unicode(256)),
        sa.Column("description", sa.UnicodeText),
        sa.Column("tags", sa.UnicodeText),
        sa.Column("used", sa.DateTime),
    )

    def init_db(self):
        """
        Initialise the database connection.
        To be called once per session.
        """

        self.engine = sa.create_engine(
            os.environ.get(
                "FLAGS_DB",
                "postgresql+psycopg2cffi:///flags",
            ),
        )
        self.metadata.create_all(self.engine)
        self.connection = self.engine.connect()

    def create(self, name, flagtype, **kwargs):
        """
        Create a new flag of the give type.
        """

        query = self.flags.insert().values(name=name, type=flagtype, **kwargs)
        self.connection.execute(query)

    def exists(self, name):
        """
        Given a flags name, check if it exists in the store.
        """

        query = sa.select([sa.exists().where(self.flags.c.name == name)])
        res = self.connection.execute(query).fetchone()
        return res[0]

    def load(self, name, flagtype):
        """
        Load a flag's value given its name. Updates the last used date.
        """

        field = f"value_{flagtype.value}"

        with self.connection.begin():
            query = sa.select([self.flags.c.get(field)]).\
                where(self.flags.c.name == name)
            data = self.connection.execute(query).fetchone()

            query = self.flags.update().\
                where(self.flags.c.name == name).\
                values(used=sa.func.now())
            self.connection.execute(query)

            return data[field]

    def store(self, name, value, flagtype):
        """
        Store a new value for a flag, given its name.
        """

        field = f"value_{flagtype.value}"

        query = self.flags.update().\
            where(self.flags.c.name == name).\
            values(**{field: value})
        self.connection.execute(query)

    def used(self, name):
        """
        Return a flag's last used date.
        """

        query = sa.select([self.flags.c.used]).\
            where(self.flags.c.name == name)
        return self.connection.execute(query).fetchone()["used"]

    def info(self, name):
        """
        Return a flag's full information.
        """

        query = sa.select([self.flags]).\
            where(self.flags.c.name == name)
        return self.connection.execute(query).fetchone()

    def all(self):
        """
        Return all flags.
        """

        query = sa.select([self.flags.c.name])
        return [
            row.name
            for row in self.connection.execute(query).fetchall()
        ]


DefaultStorage = SQLStorage()
