import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyCEDLAR",
    version="1.0.0",
    author="Zsolt Elter",
    description="pyCEDLAR: Package to estimate Cumulative Effective dose and Lifetime Attributable Risk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ezsolti/pyCEDLAR",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "numpy",
        "scipy"
    ]
)
