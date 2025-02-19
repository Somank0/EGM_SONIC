#!/usr/bin/bash
cd /eos/user/s/sosaha/EGM_test_Sonic/CMSSW_13_3_3/src/Test/Electron_RefinedRecHit_NTuplizer/python;
export HOME=/afs/cern.ch/user/s/sosaha
source /cvmfs/cms.cern.ch/cmsset_default.sh

cmsenv;
files=('root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18RECO/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/270004/22C4E1FC-D896-2345-B4F5-05CAD89E343E.root')
for i in ${files[@]};
do
cmsRun Electron_AOD_Ntuplizer_cfg.py inputFile=${i} RegressionType='BDT' 
echo 'Skimming Done'
done


