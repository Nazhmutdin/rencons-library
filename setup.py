from setuptools import setup, find_packages


setup(
    name='naks_library',
    packages=find_packages(exclude=["_types"]),
)
