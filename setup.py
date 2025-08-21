from setuptools import setup

version = '0.0.0+develop'

with open('requirements.txt') as requirements:
    install_requires = requirements.read().split()

    setup(
        name='iposconnect',
        version=version,
        author='Apriliansyah Idris',
        author_email='apriliansyahidris@gmail.com',
        description="Unofficial Python Client for iPos",
        install_requires=install_requires,
        license='MIT license'
    )
