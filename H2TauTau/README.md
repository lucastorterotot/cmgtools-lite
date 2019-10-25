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

## Running our analysis in heppy

Small interactive test: 

```
cd CMGTools/H2TauTau/cfgPython/mt
heppy Trash tauMu_2019_modular_cfg.py -N 1000 -f 
```

## Postprocessing (harvest etc)

Postprocessing is performed in Lyon on the ntuples produced by heppy and stored on the storage element (SE). 

It consists in the following steps: 

* harvesting
* postprocessing such as: skimming, adding fake method information, etc. 

During the life of a dataset, information is stored and accumulated in a MongoDB database, managed by a server running on lyovis10. 

Preprocessing has to run on a machine with access to: 

* the SE
* the /gridgroup directory, where we store our post-processed datasets.

So e.g. lyouicms1 or 2. To be tested on the slurm cluster. 

### Installation and environment

Since MongoDB is not available in the version of python distributed with CMSSW, we need to extend our version of python. 

First, **set up your CMSSW release** as explained in the main installation recipe above. 

Then, **install miniconda** with the installer that can be found [here](https://docs.conda.io/en/latest/miniconda.html) for:

* python 2.7 (must be the same major version as CMS, so any 2.7.X will do)
* Linux 64 bit (which is the same as lyouicms)

**Install pymongo with conda**. The package ends up (in my case) in `/home/cms/cbernet/miniconda2/lib/python2.7/site-packages`. Find this directory in your case, it should contain `pymongo`.

**Add this directory in front of your PYTHONPATH**, so that packages are first found here before looking in CMSSW python:

```
export PYTHONPATH=/home/cms/cbernet/miniconda2/lib/python2.7/site-packages:$PYTHONPATH
```

Test that you can import pymongo (out of the site-packages directory): 

```
python -c 'import pymongo; print(pymongo)'

>>
<module 'pymongo' from '/home/cms/cbernet/miniconda2/lib/python2.7/site-packages/pymongo/__init__.pyc'>
```

For later, you may want to add this export in your `~/.bash_profile`, so that you get the variable set properly when you log in. 

### Database connection through an ssh tunnel, and password

We're not allowed to install a server on lyouicms, but we could do it on lyovis10. Also, lyovis10 cannot be directly accessed from lyouicms.

So we need to setup an ssh tunnel from lyouicms to lyovis10 for the connection to the database. 

From lyouicms, do: 

```
ssh -L 27017:lyovis10:27017 lyoserv
```

This redirects the mongodb port (27017) on the local machine to lyovis10:27017, the port on which the mongodb server is listening to. The tunnel goes through lyoserv. 

If this command gives: 

```
bind: Address already in use
channel_setup_fwd_listener: cannot listen to port: 27017
Could not request local forwarding.
```

It certainly means that one of us has already setup the tunnel. That's good, you can use it. But the other user should not kill the connection... Ask on the mattermost team channel. 

**password:**

We have a reader and a writer password. Ask a member of the team. 

### Harvesting

Do 

```
harvest.py -h 
```

to see how to use the script. 

example of use (try it it will do nothing): 

```
harvest.py /gridgroup/cms/htt/harvest -p tt_generic_bg_Btagging_up -w 10 -n
```

remove the `-n` flag when you're sure you're ready to run.


### The dataset database 

To be written: 

* show a dataset entry 
* explain name, tiers
* explain how to connect to the DB

###

## Creation of MINIAOD_CL (Obsolete)

**For now, this step is not necessary for the 2017 analysis**

**Not finalized yet, TODO:**

* provide a vanilla CMSSW release, without CMG tools, for the production of these datasets. the tools and and the instructions will be moved to the sync repository on gitlab
* study the event content in details, and make sure that the necessary products are indeed kept, and that the old ones are dropped.  

In the new computing model, we do not run the preprocessor anymore in heppy. 
Instead, we perform some of the tasks that were done by the preprocessor with cmsRun directly, and produce MINIAOD_CL events. These events are later on read with heppy. They are common to all analysis channels. 

Set up your environment for GRID usage, and go to the `crab` directory: 

```
cd $CMSSW_BASE/src/CMGTools/H2TauTau
source ./init.sh
cd crab 
```

Set up a link to the cmsRun configuration file for the production of MINIAOD_CL events: 

```
ln -s ../python/h2TauTauMiniAOD_any_cfg.py preprocessor_cfg.py
```

**The first thing to do is ALWAYS to check that cmsRun runs locally with this configuration before submitting any job:** 

```
cmsRun preprocessor_cfg.py
```

Initialize your proxy:

```
voms-proxy-init -voms cms
```

To submit production tasks to the GRID, we use `crabSubmit.py`. Read the documentation of this script carefully:

```
crabSubmit.py -h 
```

Check available samples matching a given pattern: 

```
listhttsamples.py '*BB*'
>
[HiggsSUSYBB450:/SUSYGluGluToBBHToTauTau_M-450_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM,
 HiggsSUSYBB400:/SUSYGluGluToBBHToTauTau_M-400_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM,
... 
```

Let's narrow the choice to the sync sample: 

```
listhttsamples.py HiggsSUSYBB1000
[HiggsSUSYBB1000:/SUSYGluGluToBBHToTauTau_M-1000_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM]
```

Create a CRAB task for this sample (always use the `-n` option until you are sure about what you are going to submit):

```
crabSubmit.py HiggsSUSYBB1000 -e 10000 -n 
Task:   /SUSYGluGluToBBHToTauTau_M-1000_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM
        files/job = 1
        n jobs    = 9
```

If you're happy with the result (1 task with 9 jobs, each job reading 1 input file), remove the `-n` option to submit: 

```
crabSubmit.py HiggsSUSYBB1000 -e 10000  
```

After submission, use 

```
crab status 
```

To get the links to the dashboard, where you'll be able to follow your jobs.

