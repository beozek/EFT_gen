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

root_file_path="root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/120000/${1}"

# xrdcp -f root://cmseos.fnal.gov//store/user/beozek/EFT_gen/EFT_nanofiles_fully_semileptonic.py .
xrdcp -f /nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_27/src/EFT_gen_old/UL_beforentuple/UL_powheg.py .
python UL_powheg.py "$root_file_path"
# xrdcp -r condor_plots root://cmseos.fnal.gov//store/user/beozek/EFT_gen/
