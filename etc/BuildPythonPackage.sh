#!/usr/bin/env bash
./etc/ManylinuxDependencyInstaller.sh
ln -sf /usr/local/bin/tclsh8.6 /usr/local/bin/tclsh
yum install -y tcl-tclreadline-devel-2.1.0 tcl-tclreadline-2.1.0
pip3 install swig==4.0.2


