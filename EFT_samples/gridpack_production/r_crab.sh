#!/bin/sh

dir="/eos/uscms/store/user/beozek/EFT_gen/"

python r_crab.py $@  --production_label PNet_TT01j1l_HT800-ext --unitsPerJob 10 --totalUnits 10 --publish --gridpackDir ${dir} --gridpack TT01j1l_HT800_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz 
