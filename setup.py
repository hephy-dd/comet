from setuptools import setup, find_packages

setup(
    name='comet',
    version='0.2.3',
    author="Bernhard Arnold",
    author_email="bernhard.arnold@oeaw.ac.at",
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'PyVISA',
        'PyVISA-py',
        'PyVISA-sim',
        'PyQt5>=5.13',
        'PyQtChart>=5.13',
    ],
    package_data={
        'comet': [
            'assets/icons/*.svg',
            'widgets/*.ui',
        ],
    },
    test_suite='tests',
    license="GPLv3",
)
