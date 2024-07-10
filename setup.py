from setuptools import setup, find_packages
from pathlib import Path


VERSION = "0.0.1"
DESCRIPTION = "Getimg API Autoreg"
LONG_DESCRIPTION = Path(__file__).cwd().joinpath("README.md").read_text()


setup(
    name="getimg_api_autoreg",
    version=VERSION,
    author="Danil Krivoshapkin",
    author_email="deadcardinal293@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        "httpx",
        "disposablemail @ git+https://github.com/cardisnotvalid/disposablemail-api",
    ],
    keywords=[
        "python",
        "api",
        "api-wrapper",
        "autoreger",
        "autoregister",
        "getimg",
        "getimg-api"
    ],
)
