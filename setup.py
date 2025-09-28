import os

import pip
from setuptools import setup
from setuptools.command.install import install

PACKAGE_NAME = "iposconnect"

__version__ = '2025.09.29'

SOURCES = {
    "iposconnect-dataframe": "iposconnect-dataframe",
}


class InstallCmd(install):
    """Add custom steps for the installation command"""

    def run(self):
        wd = os.getcwd()
        for k, v in SOURCES.items():
            try:
                os.chdir(os.path.join(wd, v))
                pip.main(["install", "."])
            except Exception as e:
                print("Subhanallah, something went wrong installing", k)
                print(e)
            finally:
                os.chdir(wd)
        install.run(self)


setup(
    title="Iposconnect",
    name=PACKAGE_NAME,
    version=__version__,
    author='Apriliansyah Idris',
    author_email='apriliansyahidris@gmail.com',
    description="Unofficial Python API for iPos Desktop",
    url="https://github.com/DeeloaSociety/iposconnect",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT license",
    cmdclass={"install": InstallCmd},
)
