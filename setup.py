from setuptools import setup, find_packages
import platform


if platform.python_implementation() == "PyPy":
    _PGSQL_DRV = ["psycopg2cffi==2.7.6"]
else:
    _PGSQL_DRV = ["psycopg2==2.7.3.1"]

_REQUIRES = [
    "cornice==2.4.0",
    "pyramid==1.9.1",
    "SQLAlchemy==1.1.13",
    "zope.interface==4.4.2",
] + _PGSQL_DRV


setup(
    name="Ensign",
    version="17.9.1",
    description="Feature flag management framework and utilities",
    license="ISC",
    author="Marshland",
    author_email="dev@marshland.es",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=_REQUIRES,
    include_package_data=True,
    python_requires=">=3.5",
    zip_safe=False,
    entry_points={
        "paste.app_factory": [
            "main = ensign.api:main",
        ],
    },
)
