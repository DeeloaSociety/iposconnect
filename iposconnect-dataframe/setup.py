from setuptools import setup

PACKAGE_NAME = "dataframe"

plugin_requires = [
    "dotenv==0.9.9",
    "pandas==2.3.2",
    "ibis-framework[duckdb,postgres]==10.8.0",
    "skforecast==0.18.0",
    "lightgbm==4.6.0",
]

__version__ = "2025.09.29"

setup(
    title="Iposconnect Dataframe",
    name=f"iposconnect-{PACKAGE_NAME}",
    version=__version__,
    author="Apriliansyah Idris",
    author_email="apriliansyahidris@gmail.com",
    description="Dataframe for Iposconnect",
    url="https://github.com/DeeloaSociety/iposconnect/tree/develop/iposconnect-dataframe",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=[f"iposconnect.{PACKAGE_NAME}"],
    install_requires=plugin_requires,
    license="MIT license",
    python_requires=">=3.10",
)
