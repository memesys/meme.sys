from setuptools import setup, find_packages

setup(
    name="memesys",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.11,<4.0",
    install_requires=[
        line.strip()
        for line in open("requirements.txt")
        if line.strip() and not line.startswith("#")
    ],
    author="Kirill Korikov",
    author_email="korikov.kirill@gmail.com",
    description="Memes systems - semantic memes search telegram bot",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            'memesys=memesys.bot:main',
        ],
    },
)