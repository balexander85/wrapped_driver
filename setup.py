"""setup.py

Used for packaging wrappeddriver
"""
from pathlib import Path
from setuptools import find_packages, setup

AUTHOR = "Brian Alexander"
AUTHOR_EMAIL = "brian@dadgumsalsa.com"
REPO_URL = "https://github.com/balexander85/wrappeddriver"
VERSION = "0.2.5"
DESCRIPTION = "A simple wrapper for selenium webdriver."

with Path(__file__).parent.joinpath("README.md").open(encoding="UTF-8") as readme:
    README = readme.read()

setup(
    name="wrappeddriver",
    version=VERSION,
    packages=find_packages(),
    install_requires=["selenium>=4.1.0"],
    python_requires=">=3.8.0",
    include_package_data=False,
    license="MIT License",
    description=DESCRIPTION,
    long_description=README,
    url=REPO_URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Selenium",
        "Framework :: Selenium :: 4.1",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
    ],
)
