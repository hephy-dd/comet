from setuptools import setup, find_packages

setup(
    name='comet',
    version='1.0.dev0',
    author="Bernhard Arnold",
    author_email="bernhard.arnold@oeaw.ac.at",
    description="Control and Measurement Toolkit",
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'PyVISA==1.11.*',
        'PyVISA-py==0.5.*',
        'PyVISA-sim==0.4.*',
        'pyserial==3.5.*',
        'pyusb==1.2.*',
        'numpy==1.19.*',
        'pint==0.17.*'
    ],
    tests_require=[],
    package_data={},
    test_suite='tests',
    license="GPLv3",
)
