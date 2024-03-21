#!/bin/sh

dir="/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_27/src/EFT_gen_old/EFT_samples/nanogen_folder/nanogen_generation/NoHT/"

python launch_GEN.py $@ --production_label TT01j1lCA_NoHT --unitsPerJob 2500 --totalUnits 1000000 --publish --gridpackDir ${dir} --gridpack TT01j1lCA_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz
