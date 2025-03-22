"""Setup configuration for SynthLang CLI."""
from pathlib import Path
from setuptools import setup, find_packages

# Read version from package __init__.py
def get_version():
    """Get package version."""
    init_path = Path("synthlang") / "__init__.py"
    with open(init_path) as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip('"\'')
    raise RuntimeError("Version not found")

# Read README for long description
def get_long_description():
    """Get package long description."""
    with open("README.md", encoding="utf-8") as f:
        return f.read()

setup(
    name="synthlang",
    version=get_version(),
    description="Command-line interface for the SynthLang framework using DSPy",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="SynthLang Team",
    author_email="team@synthlang.org",
    url="https://github.com/ruvnet/SynthLang",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "click>=8.1.7",
        "dspy-ai>=2.0.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.5.2",
        "rich>=13.7.0"
    ],
    entry_points={
        "console_scripts": [
            "synthlang=synthlang.cli:cli"
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Text Processing :: General",
    ],
    keywords="ai, nlp, prompt-engineering, code-generation, framework-translation",
    project_urls={
        "Documentation": "https://synthlang.org/docs",
        "Source": "https://github.com/ruvnet/SynthLang",
        "Issues": "https://github.com/ruvnet/SynthLang/issues",
    }
)
