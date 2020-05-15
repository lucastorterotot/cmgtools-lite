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

# first make a fork from git@github.com:Arc-Pintade/cmg-cmssw.git to get cmg-cmssw.

# add your (forked) CMSSW repo
git remote add <YOUR NAME> git@github.com:<YOUR USER NAME>/cmg-cmssw.git

# add my CMSSW repo
git remote add aure git@github.com:Arc-Pintade/cmg-cmssw.git -f -t master_9_4_11_cand1_v1

# configure the sparse checkout, and get the base heppy packages
cp /afs/cern.ch/user/c/cbern/public/HTT/sparse-checkouts/sparse-checkouts-htt_9_4_11_cand1_v1 .git/info/sparse-checkout
git checkout -t aure/master_9_4_11_cand1_v1

# get my CMGTools subsystem from the cmgtools-lite repository
git clone -o aure git@github.com:Arc-Pintade/cmgtools-lite.git -b ttbar_9_4_11_cand1_v1 CMGTools

# eventually, add your (forked) repo
cd CMGTools
git remote add <YOUR NAME> git@github.com:<YOUR USER NAME>/cmgtools-lite.git
git fetch <YOUR NAME>
cd -

# get the recoil correction interface
git clone https://github.com/CMS-HTT/RecoilCorrections.git  HTT-utilities/RecoilCorrections 

# compile
scram b -j 20
```

## In practice

The idea of this code is, at the end, to create a ROOT flat tree containing all wanted observable of selected events.

In practice, hearts of the code are the config files in `CMGTools/TTbarTime/cfgPython/YOUR_CHANNEL/`
In these files, you can make selection on you events, get observable from AOD, MINIAOD, NanoAOD,... or create new ones.
Config file call all modules needed for your analysis (call Analyzers) present in `CMGTools/TTbarTime/python/heppy/` or `CMGTools/TTbarTime/python/proto/`.

## Start with heppy

The first thing to do is to run init.sh script to source everything needed and init voms

```
cd CMGTools/TTbarTime/
source ./init.sh 
```

## Running our analysis in heppy

Let's try the code with small interactive test: 

```
cd CMGTools/TTbarTime/cfgPython/me/
heppy Trash emu_cfg.py -o test=True -o year=2017 -N 1000 -f
```
This command will launch heppy in test mode (On a small part of MiniAOD), for 2017, and shut the run at 1000 events. 
All results including rootfiles will be store in the `Trash` directory.


## Running analysis with crab
When your config file is ready you can launch heppy with crab. 
Don't forget to disable the 'test' mode in your config file with :
```
test = getHeppyOption('test', False)
```
To work with crab, for this go in crab directory and run heppy :
```
cd CMGTools/TTbarTime/cfgPython/crab/
./heppy_crab.py --siteWhitelist='T3_FR_IPNL' ../me/electronMuon_2017_config.py -l "name_of_your_jobs" 
```
You can check the status of your crab jobs and resubmit jobs with :
```
cd CMGTools/TTbarTime/cfgPython/crab/
bash status_all.sh "name_of_your_jobs"
bash resubmit_all.sh "name_of_your_jobs"
```
When it's done, you can bring back your jobs on your session : 
```
cd CMGTools/scripts/
python multiHarvest.py -l "name_of_your_jobs"
```
NB: if your username is different on lxplus and on local computer add a username option on multiHarvest : 
```
python multiHarvest.py -u "lxp username" -l "name_of_your_jobs"
```
