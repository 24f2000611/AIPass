"""Fallback setup.py for older pip versions."""

from setuptools import find_packages, setup

setup(
    name="trinity-pattern",
    version="1.0.0",
    packages=find_packages(include=["trinity_pattern*"]),
    python_requires=">=3.8",
    description="Persistent identity for AI agents.",
    license="MIT",
)
