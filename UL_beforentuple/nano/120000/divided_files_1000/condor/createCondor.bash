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

for file in /nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_27/src/EFT_gen_old/UL_beforentuple/nano/120000/divided_files_1000/*.root; do
    echo "arguments = $(basename $file)" >> condor_job.sub
    echo "Queue" >> condor_job.sub
done
