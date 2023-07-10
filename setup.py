from setuptools import setup

setup(
    name="odpydoc",
    version="0.1",
    description="cursory Python package documentation",
    url="https://github.com/markmbaum/odpydoc",
    author="Mark Baum",
    packages=["odpydoc"],
    install_requires=[
        "pygments",
    ],
    include_package_data=True
)
