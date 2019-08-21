import os
import importlib
from setuptools import setup, find_packages

package = 'comet'
package_dir = os.path.join(os.path.dirname(__file__), package)

version = importlib.import_module(package, os.path.join(package_dir, '__init__.py')).__version__

setup(
    name=package,
    version=version,
    author="Bernhard Arnold",
    author_email="bernhard.arnold@oeaw.ac.at",
    packages=find_packages(),
    install_requires=[
        'PyVISA',
        'PyVISA-py',
        'PyVISA-sim',
        'Pint>=0.9',
        'PyQt5',
        'PyQt5-sip',
        'pyqtgraph',
    ],
    include_package_data=True,
    package_data={
        '': [
            'assets/icons/*.svg',
            'widgets/*.ui',
        ],
    },
    license="GPLv3",
)
