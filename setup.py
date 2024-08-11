import setuptools

with open("requirements.txt") as f:
    required = f.read().splitlines()

setuptools.setup(
    name="EmbedTAD",
    version="1.0.0",
    author="H M A Mohit Chowdhury",
    author_email="hchowdhu@uccs.edu",
    description="An efficient pipeline for TAD clustering",
    packages=setuptools.find_packages(),
    install_requires=required,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8.10",
)
