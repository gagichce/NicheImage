import re
import os
import codecs
import pathlib
from os import path
from io import open
from setuptools import setup, find_packages
from pkg_resources import parse_requirements


def read_requirements(path):
    with open(path, "r") as f:
        requirements = f.read().splitlines()
        processed_requirements = []

        for req in requirements:
            # For git or other VCS links
            if req.startswith("git+") or "@" in req:
                pkg_name = re.search(r"(#egg=)([\w\-_]+)", req)
                if pkg_name:
                    processed_requirements.append(pkg_name.group(2))
                else:
                    # You may decide to raise an exception here,
                    # if you want to ensure every VCS link has an #egg=<package_name> at the end
                    continue
            else:
                processed_requirements.append(req)
        return processed_requirements


here = path.abspath(path.dirname(__file__))
# requirements = read_requirements(os.path.join(here, "requirements.txt"))
requirements = [
    "bittensor==6.5.0",
    "cryptography==41.0.3",
    "diffusers==0.25.0",
    "ImageHash==4.3.1",
    "loguru==0.7.0",
    "numpy==1.26.3",
    "Pillow==10.2.0",
    "pydantic==1.10.13",
    "PyYAML==6.0.1",
    "Requests==2.31.0",
    "setuptools==68.0.0",
    "slowapi==0.1.8",
    "tqdm==4.65.0",
    "transformers==4.35.2",
    "omegaconf==2.3.0",
]
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# loading version from setup.py
with codecs.open(
    os.path.join(here, "nicheimage/__init__.py"), encoding="utf-8"
) as init_file:
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]", init_file.read(), re.M
    )
    version_string = version_match.group(1)

setup(
    name="nicheimage",
    version="0.0.6",
    description="NicheImage - Subnet 23 - Bittensor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NicheTensor/NicheImage",
    author="NicheImage dev",
    packages=find_packages(include=["nicheimage", "nicheimage.*"]),
    py_modules=["nicheimage"],
    package_data={"nicheimage.services.configs": ["model_config.yaml"]},
    include_package_data=True,
    author_email="",
    license="MIT",
    python_requires=">=3.8",
    install_requires=requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        # Pick your license as you wish
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
