
# PyOpenROAD

[English](README.md) | [中文](README_CN.md)

**PyOpenROAD (PyOR)** is an **unofficial** Python interface library for [OpenROAD](https://github.com/The-OpenROAD-Project/OpenROAD), packaged as a standard `.whl` file that can be installed via `pip`. This removes the need for complex dependency installation and compilation processes, allowing users to easily integrate OpenROAD into their local Python environment.

## Project Overview

This project provides a more flexible and lightweight way to access OpenROAD's functionalities:

1. No need to use OpenROAD's official pre-built packages or container images. This package works on most mainstream Linux distributions without depending on a specific one.
2. In addition to the OpenROAD binary executable, the internal Python API provided by its embedded interpreter is also wrapped as a standard Python module. This allows users to import and use OpenROAD directly in any Python script, without launching the special `openroad -python` interpreter.
3. The project includes the upstream OpenROAD repository as a Git submodule, so theoretically it supports building and packaging any version of OpenROAD (although this has not been thoroughly tested). You may manually switch the submodule commit and rebuild the `.whl` file to match the version you need.

- Current OpenROAD commit hash: `a008522d88b669ac4c985609533cf5a3d2649222`

## Installation

### Direct Installation via pip (Recommended)

Download the appropriate `.whl` file for your Python version from the [Releases](https://github.com/ZhaojieTu/PyOpenROAD/releases) page, then install it with:

```bash
pip install xxx.whl
````

### Build Locally

#### System Requirements

- Dependencies: Same as those listed in the official OpenROAD project
    

```bash
./etc/DependencyInstaller.sh
```

#### Build and Install

```bash
# Clone the repository (including submodules)
git clone --recursive https://github.com/ZhaojieTu/PyOpenROAD.git
cd PyOpenROAD

# Build and install
mkdir build
cd build
cmake ..
make
make pip_install  # Installs the built Python package into your local Python environment
```

## Usage Example

After installation, you can use OpenROAD in two ways:

1. Launch the CLI:

```bash
openroad --version
```

2. Use it in a Python script, for example `python test.py`:

```python
from openroad import Design, Tech
import odb 

tech = Tech()

tech.readLef("path/to/tech.lef")
tech.readLef("path/to/cell.lef")

design = Design(tech)

design.readDef("path/to/design.lef")

design.writeDb("path/to/design.odb")
```

