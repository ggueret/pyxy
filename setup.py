import os
from setuptools import setup
from pyxy import __VERSION__

BASEDIR_PATH = os.path.abspath(os.path.dirname(__file__))

setup(
    name="pyxy",
    version=__VERSION__,
    author="Geoffrey GUERET",
    author_email="geoffrey@gueret.tech",

    description="pyxy cache proxy.",
    long_description=open(os.path.join(BASEDIR_PATH, "README.md"), "r").read(),
    url="https://github.com/ggueret/pyxy",
    license="MIT",

    packages=["pyxy"],
    include_package_data=True,
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Framework :: Pelican",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
