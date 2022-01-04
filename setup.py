import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mc_boomer",
    version="0.0.1",
    author="Bryan Glazer",
    author_email="bryan.glazer@vanderbilt.edu",
    description="Monte Carlo Tree Search for Synthesizing Boolean Models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bglazer/mc_boomer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
