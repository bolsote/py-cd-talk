# pylint: disable=invalid-name,missing-docstring,unused-argument

import uuid

import pytest

from ensign import BinaryFlag, DefaultStorage


@pytest.mark.benchmark
def test_benchmark_flag_creation(benchmark, db):
    def create_flag():
        name = str(uuid.uuid4())
        BinaryFlag.create(name)
        return name

    result = benchmark(create_flag)
    assert DefaultStorage.exists(result)


@pytest.mark.benchmark
def test_benchmark_load(benchmark, db):
    flag = BinaryFlag.create("flag0")
    flag.set()

    def load_flag(f):
        return f.value

    result = benchmark(load_flag, flag)
    assert result


@pytest.mark.benchmark
def test_benchmark_store(benchmark, db):
    flag = BinaryFlag.create("flag0")

    def store_flag(f):
        f.value = True

    benchmark(store_flag, flag)
    assert flag.value
