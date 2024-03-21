#!/bin/bash

FILE=$1

source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /nfs/dust/cms/user/beozek/EFT/CMSSW_10_6_27/src
eval `scramv1 runtime -sh`

python EFT_nanofiles_fully_semileptonic.py $FILE
