# Import necessary functions from setuptools for packaging
from setuptools import setup, find_packages

# Call the setup() function to define your package details
setup(
    name="MLOps-pipelines",  # The name of your package (used during installation)
    version="0.0.1",          # The version of your package (follow semantic versioning)
    author="Robin Rawat",     # The author's name (you!)
    author_email="robinrawatchetry@gmail.com",  # Your contact email for users of the package

    # Automatically find all sub-packages inside your project directory that contain an __init__.py file
    # For example, src/components/, src/utils/, etc.
    packages=find_packages()
)
