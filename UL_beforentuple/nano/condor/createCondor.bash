#!/bin/bash

cat > condor_job.sub <<EOL
Universe = vanilla
Executable = run_on_condor.sh
output = \$(Cluster)_\$(Process).out
error = \$(Cluster)_\$(Process).err
log = \$(Cluster)_\$(Process).log
Transfer_Input_Files = UL_nano_fully_semileptonic_multiprocess.py
WhenToTransferOutput = ON_EXIT
EOL

for file in root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18NanoAODv9/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/120000/0520A050-AF68-EF43-AA5B-5AA77C74ED73.root; do
    echo "arguments = $(basename $file)" >> condor_job.sub
    echo "Queue" >> condor_job.sub
done
