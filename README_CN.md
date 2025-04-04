# PyOpenROAD

[English](README.md) | [中文](README_CN.md)

PyOpenroad(PyOR)是**非官方**的[OpenROAD](https://github.com/The-OpenROAD-Project/OpenROAD)的外部Python库，可以直接通过`pip install`安装在本地的Python解释器中，而不是只能在OpenROAD环境中使用。

## 项目简介

本项目提供了一种简便方式，让用户能够在自己的Python环境中调用OpenROAD的功能，而无需完全安装OpenROAD工具套件。其API使用方式和`openroad -python`启动的Python环境完全一致。

- 当前的OpenROAD版本：commit hash为`a008522d88b669ac4c985609533cf5a3d2649222`

## 安装方式

### 系统要求

- 依赖：和OpenROAD项目中的依赖一致

### 编译安装

```bash
# 克隆仓库（包括子模块）
git clone --recursive https://github.com/your-username/PyOpenROAD.git
cd PyOpenROAD

# 编译和安装
mkdir build
cd build
cmake ..
make
make pip_install  # 将编译好的Python包安装在本地的Python路径中
```

## 使用示例

安装完成后，您可以在Python中像这样使用：

```python
from openroad import Design,Tech
import odb 


tech = Tech()

tech.readLef("path/to/tech.lef")
tech.readLef("path/to/cell.lef")

design = Design(tech)

design.readDef("path/to/design.lef")

design.writeDb("path/to/design.odb")
```

