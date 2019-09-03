import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jsonquery-sebek_msd",
    version="0.0.3",
    author="Marcelo Silva",
    author_email="msilva@arkhotech.com",
    description="Prototype of query path over JSON files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arkhotech/json_query.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
