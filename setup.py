import os
import runpy
from typing import Optional, cast

from setuptools import setup


def get_version_from_pyfile(version_file: str = "yacl.py") -> str:
    file_globals = runpy.run_path(version_file)
    return cast(str, file_globals["__version__"])


def get_long_description_from_readme(readme_filename: str = "README.md") -> Optional[str]:
    long_description = None
    if os.path.isfile(readme_filename):
        with open(readme_filename, "r", encoding="utf-8") as readme_file:
            long_description = readme_file.read()
    return long_description


version = get_version_from_pyfile()
long_description = get_long_description_from_readme()

setup(
    name="yacl",
    version=version,
    py_modules=["yacl"],
    python_requires="~=3.5",
    extras_require={"colored_exceptions": ["pygments"]},
    author="Ingo Meyer",
    author_email="i.meyer@fz-juelich.de",
    description="YACL (Yet Another Color Logger) is a simple to use color logger for Python programs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/IngoMeyer441/yacl",
    keywords=["utility", "logging", "color"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development",
        "Topic :: Utilities",
    ],
)
