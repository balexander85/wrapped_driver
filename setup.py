import os
from setuptools import find_packages, setup

VERSION = "0.2.1"
DESCRIPTION = "A simple wrapper for selenium webdriver."
with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="wrappeddriver",
    version=VERSION,
    packages=find_packages(),
    install_requires=["selenium"],
    include_package_data=False,
    license="MIT License",
    description=DESCRIPTION,
    long_description=README,
    url="https://github.com/balexander85/wrappeddriver",
    author="Brian Alexander",
    author_email="brian@dadgumsalsa.com",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Selenium",
        "Framework :: Selenium :: 3.1",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires=">=3.10",
)
