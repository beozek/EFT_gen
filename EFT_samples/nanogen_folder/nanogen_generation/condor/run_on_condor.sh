#!/bin/bash
source /cvmfs/grid.desy.de/etc/profile.d/grid-ui-env.sh
source /cvmfs/cms.cern.ch/cmsset_default.sh

export SCRAM_ARCH=slc7_amd64_gcc820
scramv1 project CMSSW CMSSW_10_6_26 # cmsrel is an alias not on the workers
cd CMSSW_10_6_26/src/
eval `scramv1 runtime -sh` # cmsenv is an alias not on the workers
echo $CMSSW_BASE "is the CMSSW we created on the local worker node"
cd ${_CONDOR_SCRATCH_DIR}
pwd

root_file_path="/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_26/src/EFT_gen_old/EFT_samples/nanogen_folder/nanogen_generation/condor/TT01j1lCA_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz"

xrdcp -f /nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_26/src/EFT_gen_old/EFT_samples/nanogen_folder/nanogen_generation/condor/nanogen_cfg.py .
python nanogen_cfg.py gridpack=$root_file_path maxEvents=10
