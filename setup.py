from setuptools import setup, find_packages

setup(
    name='comet',
    version='0.13.1',
    author="Bernhard Arnold",
    author_email="bernhard.arnold@oeaw.ac.at",
    description="Control and Measurement Toolkit",
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'PyVISA>=1.10',
        'PyVISA-py',
        'PyVISA-sim',
        'pint>=0.16',
        'numpy>=1.17',
        'qutie==1.7.*',
        'QCharted==1.1.*',
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
