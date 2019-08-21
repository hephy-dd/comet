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
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'PyVISA',
        'PyVISA-py',
        'PyVISA-sim',
        'Pint>=0.9',
        'PyQt5',
        'PyQt5-sip',
        'pyqtgraph',
    ],
    package_data={
        package: [
            'assets/icons/*.svg',
            'widgets/*.ui',
        ],
    },
    test_suite='tests',
    license="GPLv3",
)
