import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="arkho-jsonquery",
    version="0.0.4",
    author="Marcelo Silva",
    author_email="msilva@arkhotech.com",
    description="Prototype of query path over JSON files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arkhotech/json_query.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Intended Audience :: Developers",
        "Natural Language :: Spanish",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules"

    ],
    python_requires='>=3.6',
)
