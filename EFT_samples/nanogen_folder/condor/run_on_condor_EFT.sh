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

root_file_path="/nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_26/src/EFT_gen_old/EFT_samples/nanogen_folder/nano_files/1j1l_NoHT_NoNu/${1}"

# xrdcp -f root://cmseos.fnal.gov//store/user/beozek/EFT_gen/EFT_nanofiles_fully_semileptonic.py .
xrdcp -f /nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_26/src/EFT_gen_old/EFT_samples/nanogen_folder/condor/EFT_nanofiles_fully_semileptonic_multiprocess_weights_nocut.py .
python EFT_nanofiles_fully_semileptonic_multiprocess_weights_nocut.py "$root_file_path"
# xrdcp -r condor_plots root://cmseos.fnal.gov//store/user/beozek/EFT_gen/
