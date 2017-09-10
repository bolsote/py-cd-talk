"""
Resources and auxiliary objects to represent flags.
"""

from cornice.resource import resource
from pyramid.httpexceptions import (
    HTTPCreated,  # 201
    HTTPNoContent,  # 204
    HTTPBadRequest,  # 400
    HTTPNotFound,  # 404
)

from ensign import BinaryFlag, FlagDoesNotExist


class FlagSchema:
    """
    Class representing a flag, to be used by the Flag resource.
    """
    # pylint: disable=too-few-public-methods

    def __init__(self, flag):
        self.name = flag.name
        self.value = flag.value
        self.active = flag.active.name
        self.label = flag.info.get("label")
        self.description = flag.info.get("description")
        self.tags = flag.info.get("tags")


@resource(path="/flags/{name}", collection_path="/flags")
class Flag:
    """
    Resource representing a Flag object. Allow to:
     - Get a flag.
     - Get all flags.
     - Create a new flag.
     - Change a flag's value.
    Flags are always referenced by name.
    """

    def __init__(self, request):
        self.request = request

    def get(self):
        """
        Get the full information for a given flag.
        """

        name = self.request.matchdict["name"]
        try:
            flag = BinaryFlag(name)
        except FlagDoesNotExist:
            raise HTTPNotFound()
        return FlagSchema(flag).__dict__

    def collection_get(self):
        """
        Get all flags in the system.
        """
        # pylint: disable=no-self-use

        return [
            FlagSchema(flag).__dict__
            for flag in BinaryFlag.all()
        ]

    def collection_post(self):
        """
        Create a new flag.
        """

        data = self.request.json_body
        try:
            name = data.pop("name")
        except KeyError:
            raise HTTPBadRequest()
        BinaryFlag.create(name, **data)
        return HTTPCreated()

    def patch(self):
        """
        Change a flag's value.
        If any other property is provided, abort.
        """

        data = self.request.json_body
        if list(data.keys()) != ["value"]:
            raise HTTPBadRequest()

        name = self.request.matchdict["name"]
        value = data.pop("value")

        try:
            flag = BinaryFlag(name)
            flag.value = value
        except FlagDoesNotExist:
            raise HTTPNotFound()

        return HTTPNoContent()
