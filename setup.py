import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stargen",
    version="1.0.1",
    author="Corey Farris",
    author_email="cfarris@protonmail.ch",
    description="A package for randomly generated star systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/farriscd/stargen",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Games/Entertainment :: Simulation",
        "Programming Language :: Python :: 3",
    ],
)
