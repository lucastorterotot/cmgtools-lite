# TTbarTime analysis of the 2017 data (CERN/Lyon)

## Installation recipe

If you work in Lyon, do the following to set up your global CMS environment:
```
source /cvmfs/cms.cern.ch/cmsset_default.sh
```

Then follow this recipe to install the analysis software: 

```
cmsrel CMSSW_9_4_11_cand1
cd CMSSW_9_4_11_cand1/src
cmsenv
git cms-init --upstream-only

# add custom CMSSW repo
git remote add lucas git@github.com:lucastorterotot/cmg-cmssw.git -f -t htt_10_4_0_v1

# configure the sparse checkout, and get the base heppy packages
cp /afs/cern.ch/user/g/gpetrucc/public/sparse-checkout_104X_heppy .git/info/sparse-checkout
git checkout -t lucas/htt_10_4_0_v1

# get the CMGTools subsystem from the cmgtools-lite repository
git clone -o lucas git@github.com:lucastorterotot/cmgtools-lite.git -b htt_10_4_0_v1 CMGTools

# get the recoil correction interface
git clone https://github.com/CMS-HTT/RecoilCorrections.git  HTT-utilities/RecoilCorrections 

#compile
scram b -j 20
```

## In practice

The idea of this code is, at the end, to create a ROOT flat tree containing all wanted observable of selected events.

```
# In practice, hearts of the code are the config files in 'CMGTools/TTbarTime/cfgPython/YOUR_CHANNEL/' 
# In these files, you can make selection on you events, get observable from AOD, MINIAOD, NanoAOD,... or create new ones.
# Config file call all modules needed for your analysis (call Analyzers) present in 'CMGTools/TTbarTime/python/heppy/' or 'CMGTools/TTbarTime/python/proto/'.  
```

## Running our analysis in heppy

Let's try the code with small interactive test: 

```
cd CMGTools/TTbarTime/cfgPython/me/
heppy Trash electronMuon_2017_config.py -o test=True -N 1000 -f

# This command will launch heppy in test mode (On a small part of MiniAOD) and shut the run at 1000 events. 
# All results including rootfiles will be store in the 'Trash' directory.
```


## Running analysis with crab

```
# When your config file is ready you can launch heppy with crab. 
# Don't forget to disable the 'test' mode in your config file with :

test = getHeppyOption('test', False)

# To work with crab, for this go in crab directory and run heppy :

cd CMGTools/TTbarTime/cfgPython/crab/
./heppy_crab.py --siteWhitelist='T3_FR_IPNL' ../me/electronMuon_2017_config.py -l "name_of_your_jobs" 

# You can check the status of your crab jobs and resubmit jobs with :

cd CMGTools/TTbarTime/cfgPython/crab/
bash status_all.sh "name_of_your_jobs"
bash resubmit_all.sh "name_of_your_jobs"

# When it's done, you can bring back your jobs on your session : 

cd CMGTools/scripts/
python multiHarvest.py -l "name_of_your_jobs"

# NB: if your username is different on lxplus and on local computer add a username option on multiHarvest : 

python multiHarvest.py -u "lxp username" -l "name_of_your_jobs"

```





```







