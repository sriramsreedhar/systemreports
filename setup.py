import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="systemreports",
    version="2.0.0",
    author="Sriram Sreedhar",
    author_email="sriramsreedhar003@gmail.com",
    description="Cross-platform system report with a local web dashboard (Windows, macOS, Linux).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sriramsreedhar/systemreports.git",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={
        "systemreports": ["templates/*.html", "static/*.css"],
    },
    install_requires=[
        "psutil>=5.9.0",
        "flask>=2.0.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "systemreports=systemreports.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
