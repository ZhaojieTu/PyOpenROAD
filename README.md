# PyOpenROAD

[English](README.md) | [中文](README_CN.md)

PyOpenROAD(PyOR) is an unofficial Python library for [OpenROAD](https://github.com/The-OpenROAD-Project/OpenROAD) that can be installed directly via `pip` into your local Python interpreter, rather than being limited to use within the OpenROAD environment.

## Project Overview

This project provides a convenient way for users to call OpenROAD functionality in their own Python environment without having to install the complete OpenROAD tool suite. Its API usage is identical to the Python environment launched with `openroad -python`.

- Current OpenROAD version: commit hash `a008522d88b669ac4c985609533cf5a3d2649222`

## Installation

### System Requirements

- Dependencies: Same as those in the OpenROAD project

### Build and Install

```bash
# Clone the repository (including submodules)
git clone --recursive https://github.com/your-username/PyOpenROAD.git
cd PyOpenROAD

# Build and install
mkdir build
cd build
cmake ..
make
make pip_install  # Installs the compiled Python package to your local Python path
```

## Usage Example

After installation, you can use it in Python like this:

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
