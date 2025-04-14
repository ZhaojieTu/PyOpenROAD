# PyOpenROAD

[English](README.md) | [中文](README_CN.md)

**PyOpenROAD (PyOR)** 是一个 **非官方** 的 [OpenROAD](https://github.com/The-OpenROAD-Project/OpenROAD) Python 接口封装项目，它将 OpenROAD 打包为一个可通过 `pip install` 安装的标准 `.whl` 文件，使用户无需繁琐的依赖安装与源码编译，即可在本地 Python 环境中快速集成使用。

## 项目简介

本项目提供一种更加灵活、轻量的方式来安装调用 OpenROAD 的各项功能：
1. 无需使用 OpenROAD 官方提供的发行包或容器镜像，安装不依赖特定 Linux 发行版，兼容主流系统。
2. 不仅包含 OpenROAD 主程序的可执行文件，同时封装了其内置 Python API，使用户可直接在任何 Python 脚本中导入并调用，而无需通过 `openroad -python` 启动环境。
3. 本项目通过 Git Submodule 引入上游 OpenROAD 仓库，理论上支持不同版本的 OpenROAD 编译打包(未进行测试)。用户可根据需求手动切换 submodule 中的 commit，并重新构建 `.whl` 包以适配特定版本。

- 当前的 OpenROAD commit hash：`a008522d88b669ac4c985609533cf5a3d2649222`

## 安装方式

### 通过pip直接安装(推荐)

在[Release](https://github.com/ZhaojieTu/PyOpenROAD/releases)中下载对应python版本的`.whl`文件,然后运行`pip install xxx.whl`进行安装


### 本地编译安装

#### 系统要求

- 依赖：和OpenROAD项目中的依赖一致
```bash
./etc/DependencyInstaller.sh
```

#### 编译

```bash
# 克隆仓库（包括子模块）
git clone --recursive https://github.com/ZhaojieTu/PyOpenROAD.git
cd PyOpenROAD

# 编译和安装
mkdir build
cd build
cmake ..
make
make pip_install  # 将编译好的Python包安装在本地的Python路径中
```

## 使用示例

安装完成后，您可以在通过如下方式使用：
1. 命令行启动`openroad`
```bash
openroad --version
```

2. 在python中调用,`python test.py`
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

