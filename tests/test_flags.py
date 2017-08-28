# pylint: disable=invalid-name,missing-docstring,no-self-use,unused-argument

import pytest

from zope.interface.verify import verifyClass

from ensign import BinaryFlag
from ensign._interfaces import IFlag, IStorage
from ensign._storage import SQLStorage


@pytest.mark.unit
class TestInterfaces:
    def test_binaryflag_implements_iflag(self):
        assert verifyClass(IFlag, BinaryFlag)

    def test_sqlstorage_implements_istorage(self):
        assert verifyClass(IStorage, SQLStorage)


@pytest.mark.unit
class TestFlagBasics:
    def test_flag_create(self, fakestore):
        flag = BinaryFlag(
            "flag0",
            store=fakestore,
        )
        flag.set()
        assert flag

    def test_flag_get_set(self, fakeflag):
        fakeflag.value = True
        assert fakeflag
        fakeflag.value = False
        assert not fakeflag


@pytest.mark.unit
class TestBinaryFlagAliases:
    def test_set(self, fakeflag):
        fakeflag.set()
        assert fakeflag

    def test_unset(self, fakeflag):
        fakeflag.unset()
        assert not fakeflag


@pytest.mark.unit
class TestFlagOperations:
    def test_flag_and(self, fakestore):
        flag0 = BinaryFlag("flag0", store=fakestore)
        flag0.unset()
        flag1 = BinaryFlag("flag1", store=fakestore)
        flag1.set()
        assert not flag0 & flag0
        assert not flag0 & flag1
        assert not flag1 & flag0
        assert flag1 & flag1

    def test_flag_or(self, fakestore):
        flag0 = BinaryFlag("flag0", store=fakestore)
        flag0.unset()
        flag1 = BinaryFlag("flag1", store=fakestore)
        flag1.set()
        assert not flag0 | flag0
        assert flag0 | flag1
        assert flag1 | flag0
        assert flag1 | flag1

    def test_flag_xor(self, fakestore):
        flag0 = BinaryFlag("flag0", store=fakestore)
        flag0.unset()
        flag1 = BinaryFlag("flag1", store=fakestore)
        flag1.set()
        assert not flag0 ^ flag0
        assert flag0 ^ flag1
        assert flag1 ^ flag0
        assert not flag1 ^ flag1

    def test_flag_not(self, fakestore):
        flag0 = BinaryFlag("flag0", store=fakestore)
        flag0.unset()
        flag1 = BinaryFlag("flag1", store=fakestore)
        flag1.set()

        assert ~flag0
        assert not ~flag1


@pytest.mark.unit
class TestFlagCall:
    def test_flag_wrapper(self, fakeflag):
        def testfun():
            return "executed"

        fakeflag.set()
        assert fakeflag(testfun)() == "executed"
        fakeflag.unset()
        assert fakeflag(testfun)() is None

    def test_flag_decorator(self, fakeflag):
        @fakeflag
        def testfun():
            return "executed"

        fakeflag.set()
        assert testfun() == "executed"
        fakeflag.unset()
        assert testfun() is None


@pytest.mark.integration
class TestSQLStorage:
    def test_create_flags(self, db):
        flag0 = BinaryFlag(
            "flag0",
            value_binary=True,
            label="Test flag 0",
            description="Flag for the purposes of testing",
            tags="test,flag",
        )
        assert flag0

    def test_get_set_flags(self, db):
        flag0 = BinaryFlag("flag0")
        assert flag0.value is None
        flag0.value = True
        assert flag0
        flag0.value = False
        assert not flag0


@pytest.mark.integration
class TestFlagsActive:
    def test_flag_new(self):
        pass

    def test_flag_active(self):
        pass

    def test_flag_inactive(self):
        pass