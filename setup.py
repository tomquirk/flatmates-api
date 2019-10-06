import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flatmates_api",
    version="0.0.1",
    author="Tom Quirk",
    author_email="tomquirkacc@gmail.com",
    description="Python wrapper for the flatmates.com.au",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tomquirk/flatmates-api",
    license='MIT',
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
