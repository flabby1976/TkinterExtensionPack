import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TkinterExtensionPack",
    version="0.0.1+dev",
    author="Andrew Robinson",
    author_email="flabby1976@gmail.com",
    description="Useful tkinter extensions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/flabby1976/TkinterExtensionPack",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU GENERAL PUBLIC LICENSE V3 OR LATER (GPLV3+)",
        "Operating System :: OS Independent",
    ],
)
