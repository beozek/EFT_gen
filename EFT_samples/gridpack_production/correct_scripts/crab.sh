#!/bin/sh

#dir="/eos/uscms/store/user/beozek/EFT_gen/"
#dir="srm://dcache-se-cms.desy.de:8443/pnfs/desy.de/cms/tier2/store/user/tiroy/EFT_Gen/"
dir="/pnfs/desy.de/cms/tier2/store/user/tiroy/EFT_Gen/"
python EFTgen_crab.py $@  --production_label TT01j1l_HT800 --unitsPerJob 2500 --totalUnits 1000000 --publish --gridpackDir ${dir} --gridpack TT01j1l_HT800_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz 
