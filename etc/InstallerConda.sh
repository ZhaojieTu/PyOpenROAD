#!/usr/bin/env bash

pushd /tmp
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda
source /opt/conda/bin/activate
popd
source /opt/conda/bin/activate
conda deactivate