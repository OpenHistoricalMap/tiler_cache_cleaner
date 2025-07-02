from setuptools import setup, find_packages

setup(
    name="tiler_cache_cleaner",
    version="0.1",
    author="Rub21",
    author_email="rub2106@gmail.com",
    description="Efficient S3 tile cache cleaner",
    packages=find_packages(),
    install_requires=["boto3", "botocore", "mercantile", "typer[all]"],
    entry_points={
        "console_scripts": [
            "tiler-cache-cleaner=tiler_cache_cleaner.cli:app",
        ],
    },
    python_requires='>=3.7',
)