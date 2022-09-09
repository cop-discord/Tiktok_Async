from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
desc = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="TikTok-Async",
    version="1.0.1",
    description="A module which allows for TikTok Video Downloading and statistics without requirement of authorization",
    long_description=desc,
    long_description_content_type="text/markdown",
    author="antinuke0day",
    url="https://github.com/antinuke0day/TikTok-Async",
    python_requires=">=3.6",
    packages=find_packages(include=["TikTok-Async", "TikTok-Async.*"]),
)