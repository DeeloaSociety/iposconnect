from setuptools import setup

PACKAGE_NAME = "orm"

plugin_requires = [
    "dotenv==0.9.9",
    "SQLAlchemy==2.0.45",
    "psycopg2==2.9.11",
]

__version__ = "2025.12.19"

setup(
    title="Iposconnect ORM",
    name=f"iposconnect-{PACKAGE_NAME}",
    version=__version__,
    author="Apriliansyah Idris",
    author_email="apriliansyahidris@gmail.com",
    description="ORM for Iposconnect",
    url="https://github.com/DeeloaSociety/iposconnect/tree/develop/iposconnect-orm",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=[f"iposconnect.{PACKAGE_NAME}"],
    install_requires=plugin_requires,
    license="MIT license",
    python_requires=">=3.10",
)
