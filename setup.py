from distutils.core import setup
from setuptools import find_packages

setup(
    name="lin-algebra",
    version="0.1",
    py_modules=["main"],
    packages=find_packages(),

    # metadata
    author="Richard Scheiwe",
    author_email="richard.s@taboola.com",
    description="linear algebra package",
    license="Public Domain",
    keywords="linear algebra"
)