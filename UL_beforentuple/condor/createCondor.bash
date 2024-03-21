#!/bin/bash

cat > condor_job.sub <<EOL
Universe = vanilla
Executable = run_on_condor.sh
output = \$(Cluster)_\$(Process).out
error = \$(Cluster)_\$(Process).err
log = \$(Cluster)_\$(Process).log
Transfer_Input_Files = EFT_nanofiles_fully_semileptonic_multiprocess.py
WhenToTransferOutput = ON_EXIT
EOL

for file in root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18MiniAODv2/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/120000/*.root; do
    echo "arguments = $(basename $file)" >> condor_job.sub
    echo "Queue" >> condor_job.sub
done
