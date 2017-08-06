from setuptools import setup, find_packages

setup(
    name="librarian",
    version="17.9.1",
    description="Application and API to manage libraries",
    author="Marshland",
    author_email="dev@marshland.es",
    packages_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
    ],
    python_requires=">=3.5",
    zip_safe=False,
)
