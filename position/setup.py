from setuptools import setup, find_packages

setup(
    name='sgfc_position',
    zip_safe = True,
    version='0.1',
    url='',
    description='',
    license='',
    author='Srdjan Grubor',
    author_email='sgnn7@sgnn7.org',
    packages=find_packages(),
    install_requires = [
        'pynmea2',
        'pyserial',
    ],
)
