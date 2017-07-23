from setuptools import setup, find_packages

setup(
    name='sgfc',
    zip_safe = True,
    version='0.1',
    url='',
    description='',
    license='',
    author='Srdjan Grubor',
    author_email='sgnn7@sgnn7.org',
    packages=find_packages(),
    install_requires = [
        'sgfc_communication',
        'sgfc_control',
        'sgfc_io'
#        'sgfc_vision',
    ],
)
