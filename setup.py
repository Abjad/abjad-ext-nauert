#! /usr/bin/env python
import pathlib

import setuptools

subpackage_name = "nauert"


def read_version():
    root_path = pathlib.Path(__file__).parent
    version_path = root_path / "abjadext" / subpackage_name / "_version.py"
    with version_path.open() as file_pointer:
        file_contents = file_pointer.read()
    local_dict = {}
    exec(file_contents, None, local_dict)
    return local_dict["__version__"]


author = ["Josiah Wolf Oberholtzer", "Tsz Kiu Pang"]

author_email = [
    "josiah.oberholtzer@gmail.com",
    "osamupang@gmail.com",
]

if __name__ == "__main__":
    setuptools.setup(
        author=", ".join(author),
        author_email=", ".join(author_email),
        classifiers=[
            "Development Status :: 3 - Alpha",
            "License :: OSI Approved :: GNU General Public License (GPL)",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: Implementation :: CPython",
            "Topic :: Artistic Software",
        ],
        extras_require={
            "test": [
                "black>=20.8b1",
                "flake8>=3.8.2",
                "isort>=4.3.21",
                "mypy>=0.770",
                "pytest>=5.4.3",
                "pytest-cov>=2.6.0",
                "pytest-helpers-namespace",
            ]
        },
        include_package_data=True,
        install_requires=["abjad==3.2"],
        license="MIT",
        long_description=pathlib.Path("README.md").read_text(),
        keywords=", ".join(
            [
                "music composition",
                "music notation",
                "lilypond",
            ]
        ),
        name="abjad-ext-{}".format(subpackage_name),
        packages=["abjadext"],
        platforms="Any",
        url="http://abjad.github.io",
        version=read_version(),
    )
