from setuptools import setup, find_packages

setup(
    name='sgfc_control',
    zip_safe = True,
    version='0.1',
    url='',
    description='',
    license='',
    author='Srdjan Grubor',
    author_email='sgnn7@sgnn7.org',
    packages=find_packages(),
    install_requires = [
        'python-steamcontroller',
    ],
    dependency_links = [
        'https://github.com/ynsta/steamcontroller/tarball/master#egg=python-steamcontroller',
    ],
)
