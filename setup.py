import setuptools

with open("requirements.txt") as f:
    required = f.read().splitlines()

setuptools.setup(
    name="EmbedTAD",
    version="1.0.0",
    author="H. M. A. Mohit Chowdhury",
    author_email="h.m.a.mohitchowdhury@my.unt.edu",
    description="An efficient architecture for TAD detection",
    packages=setuptools.find_packages(),
    install_requires=required,
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "License :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
)
