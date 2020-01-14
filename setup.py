from setuptools import setup, find_packages

setup(
    name='comet',
    version='0.5.0',
    author="Bernhard Arnold",
    author_email="bernhard.arnold@oeaw.ac.at",
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'PyVISA',
        'PyVISA-py',
        'PyVISA-sim',
        'numpy>=1.17',
        'PyQt5>=5.13',
        'QCharted>=1.1',
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
