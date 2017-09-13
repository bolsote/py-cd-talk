# pylint: disable=invalid-name,missing-docstring,no-self-use

import datetime

import pytest

from zope.interface.verify import verifyClass

from ensign import BinaryFlag
from ensign._flags import FlagActive, FlagDoesNotExist
from ensign._interfaces import IFlag, IStorage
from ensign._storage import DefaultStorage, SQLStorage, FlagTypes


@pytest.mark.unit
class TestInterfaces:
    def test_binaryflag_implements_iflag(self):
        assert verifyClass(IFlag, BinaryFlag)

    def test_sqlstorage_implements_istorage(self):
        assert verifyClass(IStorage, SQLStorage)


@pytest.mark.unit
class TestFlagBasics:
    def test_flag_create(self, fakestore):
        flag = BinaryFlag.create(
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

    def test_flag_raises_if_inexistent(self, fakestore):
        with pytest.raises(FlagDoesNotExist):
            BinaryFlag("flag42", store=fakestore)

    def test_get_all_flags(self, fakestore):
        names = ["flag0", "flag1", "flag2"]
        for name in names:
            BinaryFlag.create(name, store=fakestore)
        allflags = BinaryFlag.all(store=fakestore)
        assert len(allflags) == len(names)
        for flag in allflags:
            assert flag.name in names


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
        flag0 = BinaryFlag.create("flag0", store=fakestore)
        flag0.unset()
        flag1 = BinaryFlag.create("flag1", store=fakestore)
        flag1.set()
        assert not flag0 & flag0
        assert not flag0 & flag1
        assert not flag1 & flag0
        assert flag1 & flag1

    def test_flag_or(self, fakestore):
        flag0 = BinaryFlag.create("flag0", store=fakestore)
        flag0.unset()
        flag1 = BinaryFlag.create("flag1", store=fakestore)
        flag1.set()
        assert not flag0 | flag0
        assert flag0 | flag1
        assert flag1 | flag0
        assert flag1 | flag1

    def test_flag_xor(self, fakestore):
        flag0 = BinaryFlag.create("flag0", store=fakestore)
        flag0.unset()
        flag1 = BinaryFlag.create("flag1", store=fakestore)
        flag1.set()
        assert not flag0 ^ flag0
        assert flag0 ^ flag1
        assert flag1 ^ flag0
        assert not flag1 ^ flag1

    def test_flag_not(self, fakestore):
        flag0 = BinaryFlag.create("flag0", store=fakestore)
        flag0.unset()
        flag1 = BinaryFlag.create("flag1", store=fakestore)
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


@pytest.mark.unit
class TestFlagActive:
    def test_flag_new(self, fakestore):
        flag0 = BinaryFlag.create("flag0", store=fakestore)
        assert flag0.active == FlagActive.NEW

    def test_flag_active(self, fakestore):
        flag0 = BinaryFlag.create(
            "flag0",
            store=fakestore,
            used=datetime.datetime.now(),
        )
        assert flag0.active == FlagActive.ACTIVE

    def test_flag_inactive(self, fakestore):
        flag0 = BinaryFlag.create(
            "flag0",
            store=fakestore,
            used=datetime.datetime.now() - datetime.timedelta(days=8),
        )
        assert flag0.active == FlagActive.INACTIVE


@pytest.mark.unit
class TestFlagInfo:
    def test_basic_info(self, fakestore):
        want_info = {
            "name": "flag0",
            "label": "",
            "description": "",
            "tags": "",
        }
        flag0 = BinaryFlag.create(
            name="flag0",
            store=fakestore,
        )
        assert flag0.info == want_info

    def test_full_info(self, fakestore):
        want_info = {
            "name": "flag0",
            "label": "Fake flag",
            "description": "Flag for testing purposes",
            "tags": "test,fake",
        }
        flag0 = BinaryFlag.create(
            store=fakestore,
            **want_info,
        )
        assert flag0.info == want_info


@pytest.mark.integration
@pytest.mark.usefixtures("db")
class TestSQLBackedFlags:
    def test_create_flags(self):
        flag0 = BinaryFlag.create(
            "flag0",
            value_binary=True,
            label="Test flag 0",
            description="Flag for the purposes of testing",
            tags="test,flag",
        )
        assert flag0

    def test_flag_exists(self):
        with pytest.raises(FlagDoesNotExist):
            BinaryFlag("flag0")

    def test_get_set_flags(self):
        flag0 = BinaryFlag.create("flag0")
        assert flag0.value is None
        flag0.value = True
        assert flag0
        flag0.value = False
        assert not flag0

    def test_flag_new(self):
        flag0 = BinaryFlag.create("flag0")
        assert flag0.active == FlagActive.NEW

    def test_flag_active(self):
        flag0 = BinaryFlag.create("flag0")
        flag0.set()
        assert flag0
        assert flag0.active == FlagActive.ACTIVE

    def test_flag_inactive(self):
        flag0 = BinaryFlag.create(
            "flag0",
            used=datetime.datetime.now() - datetime.timedelta(days=8),
        )
        assert flag0.active == FlagActive.INACTIVE

    def test_flag_info(self):
        want_info = {
            "name": "flag0",
            "label": "Fake flag",
            "description": "Flag for testing purposes",
            "tags": "test,fake",
        }
        flag0 = BinaryFlag.create(**want_info)
        assert flag0.info == want_info

    def test_get_all_flags(self):
        names = ["flag0", "flag1", "flag2"]
        for name in names:
            BinaryFlag.create(name)
        allflags = BinaryFlag.all()
        assert len(allflags) == len(names)
        for flag in allflags:
            assert flag.name in names


@pytest.mark.integration
@pytest.mark.usefixtures("db")
class TestSQLStorage:
    def test_exists(self):
        DefaultStorage.create("flag0", FlagTypes.BINARY)
        assert DefaultStorage.exists("flag0")
        assert not DefaultStorage.exists("flag1")

    def test_load_store(self):
        DefaultStorage.create("flag0", FlagTypes.BINARY)
        DefaultStorage.store("flag0", True, FlagTypes.BINARY)
        assert DefaultStorage.load("flag0", FlagTypes.BINARY) is True
        DefaultStorage.store("flag0", False, FlagTypes.BINARY)
        assert DefaultStorage.load("flag0", FlagTypes.BINARY) is False

    def test_used(self):
        used = datetime.datetime.now()
        DefaultStorage.create("flag0", FlagTypes.BINARY, used=used)
        assert DefaultStorage.used("flag0") == used

    def test_get_all(self):
        names = ["flag0", "flag1", "flag2"]
        for name in names:
            DefaultStorage.create(name, FlagTypes.BINARY)
        allitems = DefaultStorage.all()
        assert len(allitems) == len(names)
        for flag in allitems:
            assert flag in names
