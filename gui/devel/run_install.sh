#!/bin/sh

wet https://repo.anaconda.com/archive/Anaconda3-2020.07-Linux-x86_64.sh
bash Anaconda3-2020.07-Linux-x86_64.sh

source ~/.bashrc

wget https://computing.docs.ligo.org/conda/environments/linux/igwn-py37.yaml
conda env create --file igwn-py37.yaml -n mifsim37

conda activate mifsim37

conda install -y -c gwoptics pykat

conda install -c conda-forge pysimplegui 

# conda uninstall -y finesse
# conda activate mifsim37; conda install -y -c gwoptics pykat
