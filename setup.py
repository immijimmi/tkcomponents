from setuptools import setup

with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name="tkcomponents",
    packages=[
        "tkcomponents", "tkcomponents.extensions", "tkcomponents.basiccomponents",
        "tkcomponents.basiccomponents.classes"
    ],
    version="3.0.0",
    license="MIT",
    description="An OOP framework for Tkinter, inspired by React",
    long_description_content_type="text/markdown",
    long_description=long_description,
    author="immijimmi",
    author_email="immijimmi1@gmail.com",
    url="https://github.com/immijimmi/tkcomponents",
    download_url="https://github.com/immijimmi/tkcomponents/archive/refs/tags/v3.0.0.tar.gz",
    keywords=[
        'ui', 'gui', 'graphical', 'user', 'interface'
    ],
    install_requires=[
        'objectextensions~=2.0.2'
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
    ],
)
