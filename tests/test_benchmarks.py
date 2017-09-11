# pylint: skip-file

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


@pytest.mark.benchmark
def test_benchmark_api_post(benchmark, db, api):
    def request():
        api.post_json(
            "/flags",
            {
                "name": str(uuid.uuid4()),
            },
            status=201,
        )
    benchmark(request)


@pytest.mark.benchmark
def test_benchmark_api_post_full(benchmark, db, api):
    def request():
        api.post_json(
            "/flags",
            {
                "name": str(uuid.uuid4()),
                "label": "Test flag",
                "description": "Fake flag",
                "tags": "test",
            },
            status=201,
        )
    benchmark(request)


@pytest.mark.benchmark
def test_benchmark_api_get(benchmark, db, api):
    BinaryFlag.create(
        "flag0",
        label="Flag",
        description="Testing flag",
        tags="test",
    )
    benchmark(api.get, "/flags/flag0", status=200)


@pytest.mark.benchmark
def test_benchmark_api_get_all(benchmark, db, api):
    for k in range(100):
        BinaryFlag.create(f"flag{k}")
    benchmark(api.get, "/flags", status=200)


@pytest.mark.benchmark
def test_benchmark_patch(benchmark, db, api):
    BinaryFlag.create("flag0")
    benchmark(api.patch_json, "/flags/flag0", {"value": True}, status=204)
