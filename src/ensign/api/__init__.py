# pylint: disable=missing-docstring, unused-argument

from pyramid.config import Configurator
from ensign import DefaultStorage


def main(global_config, **settings):
    if not global_config.get("testing"):  # pragma: no cover
        DefaultStorage.init_db()

    config = Configurator(settings=settings)
    config.include("cornice")
    config.scan("ensign.api.resources")
    return config.make_wsgi_app()
