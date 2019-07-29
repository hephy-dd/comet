import imp
from setuptools import setup, find_packages

version = imp.load_source('comet', 'comet/__init__.py').__version__

setup(
    name='comet',
    version=version,
    author="Bernhard Arnold",
    author_email="bernhard.arnold@oeaw.ac.at",
    packages=find_packages(),
    install_requires=[
        'python-statemachine',
        'pyvisa',
        'pyvisa-py',
        'pyvisa-sim',
        'lantz-core',
        'lantz-sims',
        'lantz-drivers',
    ],
    license="GPLv3",
)
