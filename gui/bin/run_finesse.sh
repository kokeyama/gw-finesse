#!/bin/bash
#
# This code is called by medm command.
# See this page as example : http://gwwiki.icrr.u-tokyo.ac.jp/JGWwiki/KAGRA/Commissioning/NoiseBudgetter
#
# cd /users/MIF/gw-finesse/gui/bin
# conda activate mifsim37
# ./run_finesse.sh
#

source /kagra/kagraups/etc/conda2-user-env.sh
conda activate mifsim37
cd /users/MIF/gw-finesse/gui/bin
python mifsim_gui.py
conda deactivate mifsim37

