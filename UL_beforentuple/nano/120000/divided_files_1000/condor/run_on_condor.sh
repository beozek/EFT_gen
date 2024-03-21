#!/bin/bash
source /cvmfs/grid.desy.de/etc/profile.d/grid-ui-env.sh
source /cvmfs/cms.cern.ch/cmsset_default.sh

export SCRAM_ARCH=slc7_amd64_gcc820
scramv1 project CMSSW CMSSW_10_6_28 # cmsrel is an alias not on the workers
cd CMSSW_10_6_28/src/
eval `scramv1 runtime -sh` # cmsenv is an alias not on the workers
echo $CMSSW_BASE "is the CMSSW we created on the local worker node"
cd ${_CONDOR_SCRATCH_DIR}
pwd

root_file_path="/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_27/src/EFT_gen_old/UL_beforentuple/nano/120000/divided_files_1000/${1}"

xrdcp -f /nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_27/src/EFT_gen_old/UL_beforentuple/nano/UL_nano_fully_semileptonic_multiprocess.py .
python UL_nano_fully_semileptonic_multiprocess.py "$root_file_path"
