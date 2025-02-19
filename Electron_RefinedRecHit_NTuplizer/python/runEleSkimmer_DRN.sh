#!/usr/bin/bash
cd /eos/user/s/sosaha/EGM_test_Sonic/CMSSW_13_3_3/src/Test/Electron_RefinedRecHit_NTuplizer/python;
export HOME=/afs/cern.ch/user/s/sosaha
source /cvmfs/cms.cern.ch/cmsset_default.sh

cmsenv;
files=('DRN_DYtoLL_file1.root')
for i in ${files[@]};
do
cmsRun Electron_AOD_Ntuplizer_cfg.py inputFile="file:../../${i}" RegressionType='DRN' 
echo 'Skimming Done'
done


