# H->tau tau analysis of the 2017 data (CERN/Lyon)

## Installation recipe

If you work in Lyon, do the following to set up your global CMS environment:
```
source /cvmfs/cms.cern.ch/cmsset_default.sh
```

Then follow this recipe to install the analysis software: 

```
cmsrel CMSSW_10_4_0
cd CMSSW_10_4_0/src
cmsenv
git cms-init --upstream-only

# add custom CMSSW repo
git remote add lucas git@github.com:lucastorterotot/cmg-cmssw.git -f -t heppy_104X_dev

# configure the sparse checkout, and get the base heppy packages
cp /afs/cern.ch/user/g/gpetrucc/public/sparse-checkout_104X_heppy .git/info/sparse-checkout
git checkout -b heppy_104X_dev lucas/heppy_104X_dev

# get the CMGTools subsystem from the cmgtools-lite repository
git clone -o lucas git@github.com:lucastorterotot/cmgtools-lite.git -b 104X_dev CMGTools

# get the recoil correction interface
git clone https://github.com/CMS-HTT/RecoilCorrections.git  HTT-utilities/RecoilCorrections 

#compile
scram b -j 20
```