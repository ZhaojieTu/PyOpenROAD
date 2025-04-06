#!/usr/bin/env bash
./etc/DependencyInstaller.sh
pip install swig==4.0.2


pushd /tmp
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda
source /opt/conda/bin/activate
popd