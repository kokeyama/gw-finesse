#!/bin/bash
# on control workstations, we can't load .bashrc except for interactive bash.
#
source ~/.bashrc

#
conda activate mifsim37

python GUI.py

