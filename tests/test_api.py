# pylint: disable=invalid-name,missing-docstring,no-self-use

import pytest

from ensign import BinaryFlag


@pytest.mark.component
@pytest.mark.usefixtures("db")
class TestFlagsAPI:
    def test_get(self, api):
        BinaryFlag.create(
            "flag0",
            label="Fake flag",
            description="Flag for testing purposes",
            tags="test,fake",
        )
        response = api.get("/flags/flag0", status=200)

        assert response.json["name"] == "flag0"

    def test_collection_get(self, api):
        names = ["flag0", "flag1", "flag42"]
        for name in names:
            BinaryFlag.create(name)
        response = api.get("/flags", status=200)

        assert len(response.json) == len(names)
        for item in response.json:
            assert item["name"] in names

    def test_post(self, api):
        payload = {
            "name": "test_flag",
            "label": "Test flag",
            "description": "Flag for testing purposes",
            "tags": "test,flag,fake",
        }
        api.post_json("/flags", payload, status=201)
        flag = BinaryFlag("test_flag")

        assert flag.info == payload

    def test_patch(self, api):
        payload = {
            "value": True,
        }
        flag = BinaryFlag.create("flag0")
        api.patch_json("/flags/flag0", payload, status=204)

        assert flag

    def test_flag_flow(self, api):
        response = api.post_json(
            "/flags",
            {"name": "flag_flow"},
            status=201,
        )

        response = api.get("/flags", status=200)
        assert len(response.json) == 1

        response = api.patch_json(
            "/flags/flag_flow",
            {"value": True},
            status=204,
        )

        response = api.get("/flags/flag_flow", status=200)
        assert response.json["value"]


@pytest.mark.component
@pytest.mark.usefixtures("db")
class TestFlagsAPIErrors:
    def test_get_404(self, api):
        api.get("/flags/flag314", status=404)

    def test_post_400_empty(self, api):
        api.post_json("/flags", {}, status=400)

    def test_post_400_noname(self, api):
        api.post_json("/flags", {
            "label": "Unnamed flag",
            "description": "No name flag",
        }, status=400)

    def test_patch_400_novalue(self, api):
        BinaryFlag.create("flag0")
        api.patch_json("/flags/flag0", {}, status=400)

    def test_patch_400_extrafields(self, api):
        BinaryFlag.create("flag0")
        api.patch_json("/flags/flag0", {
            "value": True,
            "label": "Label",
        }, status=400)

    def test_patch_404(self, api):
        api.patch_json("/flags/flag0", {
            "value": True,
        }, status=404)
