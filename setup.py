import setuptools
import os

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'VERSION')) as version_file:
    version = version_file.read().strip()

with open("README.md", "r") as readme:
    readme_content = readme.read()

setuptools.setup(
    name="majortom_scripting",
    version=version,
    author="Kubos",
    author_email="open-source@kubos.com",
    description="A package for interacting with Major Tom's Scripting API.",
    long_description=readme_content,
    long_description_content_type="text/markdown",
    url="https://github.com/kubos/majortom_scripting_package",
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.7',
    keywords='majortom major_tom script kubos major tom satellite',
)
