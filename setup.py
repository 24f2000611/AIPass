"""Fallback setup.py for older pip versions."""

from setuptools import find_packages, setup

setup(
    name="trinity-pattern",
    version="1.0.0",
    packages=find_packages(include=["trinity_pattern*"]),
    package_data={"trinity_pattern": ["templates/*.md"]},
    entry_points={"console_scripts": ["trinity=trinity_pattern.cli:main"]},
    python_requires=">=3.8",
    description="Persistent identity for AI agents.",
    license="MIT",
)
