
from setuptools import setup, find_packages
from pathlib import Path

# Lê o conteúdo de arquivos locais
this_directory = Path(__file__).parent

long_description = (this_directory / "README.md").read_text()
version = (this_directory / "VERSION").read_text()
requirements = (this_directory / "requirements.txt").read_text()

setup(
    name="safethread",
    version=version,
    packages=find_packages(exclude=["tests", "docs", "examples"]),
    python_requires=">=3.7",
    install_requires=requirements.splitlines(),
    include_package_data=True,
    author="Andre Luiz Romano Madureira",
    description="Python utilities classes for safe deployment and management of Threads, synchronization and Python data structures.",
    long_description=long_description,  # Inclui o conteúdo do README.md
    long_description_content_type="text/markdown",  # Define o tipo do conteúdo
    url="https://github.com/andre-romano/safethread",
    classifiers=[],
    keywords="threading, threads, thread-safe, process, multiprocessing, concurrent, Python",
    license="Apache-2.0",
    license_files=["LICENSE"],
)
