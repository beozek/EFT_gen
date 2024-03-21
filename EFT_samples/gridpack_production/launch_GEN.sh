#!/bin/sh

dir="/eos/vbc/group/cms/robert.schoefbeck/gridpacks/ParticleNet/"

python launch_GEN.py $@ --config gen_LO_01j_mc_102X_CP5 --production_label PNet_TT01j1l_HT800-ext --unitsPerJob 30000 --totalUnits 20000000 --publish --gridpackDir ${dir} --gridpack TT01j1l_HT800_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz 
