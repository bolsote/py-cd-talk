from setuptools import setup, find_packages

setup(
    name="Ensign",
    version="17.9.1",
    description="Feature flag management framework and utilities",
    author="Marshland",
    author_email="dev@marshland.es",
    packages_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "SQLAlchemy==1.1.13",
        "zope.intereface==4.4.2",
    ],
    python_requires=">=3.5",
    zip_safe=False,
)
