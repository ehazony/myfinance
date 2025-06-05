"""Setup script for finance_common package."""

from setuptools import setup, find_packages

setup(
    name="finance_common",
    version="0.1.0",
    description="Shared models, utilities, and database connections for finance services",
    author="Finance Team",
    packages=find_packages(),
    install_requires=[
        "SQLAlchemy>=1.4",
        "psycopg2-binary",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
) 