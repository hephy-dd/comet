from setuptools import setup, find_packages

setup(
    name='comet',
    version='0.11.2',
    author="Bernhard Arnold",
    author_email="bernhard.arnold@oeaw.ac.at",
    description="Control and Measurement Toolkit",
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'PyVISA>=1.10',
        'PyVISA-py',
        'PyVISA-sim',
        'pint>=0.10',
        'numpy>=1.17',
        'qutie>=1.5.2',
        'QCharted>=1.1',
    ],
    package_data={
        'comet': [
            'assets/icons/*.ico',
            'assets/icons/*.svg',
        ],
    },
    test_suite='tests',
    license="GPLv3",
)
