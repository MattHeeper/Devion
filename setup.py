from setuptools import setup, find_packages
from pathlib import Path

HERE = Path(__file__).parent
long_description = (HERE / "README.md").read_text(encoding="utf-8") if (HERE / "README.md").exists() else ""

setup(
    name="devion",
    version="0.1.21",
    description="Devion — Development Environment Manager (core python package)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MattHeeper/Devion",
    author="MattHeeper",
    license="Apache-2.0",
    packages=find_packages(include=["devion", "devion.*"]),
    package_dir={"": "."},
    include_package_data=True,
    install_requires=[],
    python_requires=">=3.11",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
