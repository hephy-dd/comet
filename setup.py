import os
import importlib
from PyQt5 import uic

from setuptools import setup, find_packages
from setuptools.command.build_py import build_py

package_dir = os.path.join(os.path.dirname(__file__), 'comet')

version = importlib.import_module('comet', os.path.join(package_dir, '__init__.py')).__version__

class BuildPyCommand(build_py):
    def run(self):
        uic.compileUiDir(os.path.join(package_dir, 'widgets', 'ui'))
        build_py.run(self)


setup(
    name='comet',
    version=version,
    author="Bernhard Arnold",
    author_email="bernhard.arnold@oeaw.ac.at",
    packages=find_packages(),
    install_requires=[
        'PyVISA',
        'PyVISA-py',
        'PyVISA-sim',
        'Pint>=0.9',
        'slave>=0.4',
        'PyQt5',
        'PyQt5-sip',
        'pyqtgraph',
    ],
    include_package_data=True,
    package_data={
        '': [
            'widgets/ui/*.ui',
        ],
    },
    cmdclass={
        'build_py': BuildPyCommand,
    },
    license="GPLv3",
)
