##### 
1. to run the emu file with 2016, first made the directory in :
CMGTools.TTbarTime.proto.samples.summer16 

2. copied
> 
 CMGTools.TTbarTime.proto.samples.fall17.ttbar2017 
and
 CMGTools.TTbarTime.proto.samples.fall17.trigger 
 
to summer16 and updated the samples and trigger list. For trigger used the AN-2018/043/v17. For samples used dasgoclient to find the updated list from PPD RUNII SUMMARY: 
https://docs.google.com/presentation/d/1YTANRT_ZeL5VubnFq7lNGHKsiD7D3sDiOPNgXUYVI0I/edit#slide=id.g7068f62c63_1_0 

Got the cross-sections from McM and not AN. Tried to stick with same tune as used by Aurelien for 2017 samples. Few samples that are still with the different tunes. Keep an eye on them for same tune.

Get the json from : 
https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions16/13TeV/ReReco/

Lumi number from: 
https://twiki.cern.ch/twiki/bin/view/CMS/TWikiLUM
> In lxplus bash, 
 export PATH=$HOME/.local/bin:/cvmfs/cms-bril.cern.ch/brilconda/bin:$PATH
 pip install --user --upgrade brilws
 brilcalc lumi -u /pb --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -i /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt 

Get the run range from:
 > https://twiki.cern.ch/twiki/bin/view/CMS/PdmV2016Analysis
 
To get the lumi for a given run-range
2016 B to F : 
brilcalc lumi -u /pb --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -i /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt --begin 272007 --end 278808

19695.422958521

2016 G to H :
brilcalc lumi -u /pb --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -i /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt --begin 278820 --end 284044
16226.452636126 

3. Made the emu cfg compatible to run with 2016 MC/data

4. for the JEC, got the tar files from 
https://twiki.cern.ch/twiki/bin/view/CMS/JECDataMC

for both MC and data 
and copied their content to :

CMGTools/RootTools/data/jec/

and updated the JEC tags accordingly in cfg file. 

Other helper links : 
https://github.com/cms-nanoAOD/nanoAOD-tools/blob/master/python/postprocessing/modules/jme/jetmetHelperRun2.py
https://github.com/cms-nanoAOD/nanoAOD-tools/blob/master/python/postprocessing/modules/jme/jetmetUncertainties.py


5. For the PU distributions 
For MC:
    > Run CMGTools/TTbarTime/cfgPython/weights/PileUp_config.py with crab in CMGTools/TTbarTime/cfgPython/crab/ using instructions from main README file from Aurelien. This file should be made sure to be running first with test option. 

    > Once the jobs are done, and output should be extracted locally in CMGTools/TTbarTime/scripts/ dir using multiharvest file - again the instructions to be followed in README from Aurelien

    > Then to obtain one pileup file, with histos of all MC samples in one root file, run :     
      CMGTools/TTbarTime/weights/pileup/pu_hist_gen.py
      with usuage explained in the file itself. Please note, if -g is by default false, so one has to put -g as option, if you want to copy the root files here in this dir locally first. Ultimates it generates the file and copies it in CMGTools/TTbarTime/data/ dir.  
    

For Data: 
 
 > Get the root file with required binning (in our case 200 bins) using commandline from: 
#https://twiki.cern.ch/twiki/bin/view/CMS/PileupJSONFileforData

pileupCalc.py -i Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt --inputLumiJSON pileup_latest.txt --calcMode true --minBiasXsec 69200 --maxPileupBin 200 --numPileupBins 200 MyDataPileupHistogram.root

get the pileup_latest.txt from : 
https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions16/13TeV/PileUp/
 


6. For Muon SFs: 

> Copy all the SF files from 
https://twiki.cern.ch/twiki/bin/view/CMS/MuonReferenceEffs2016LegacyRereco

to data/2016/muonSF/ and data/2016/muonSF/SystUnc/

> Update MuonSFARC.py  to extract SF as event weights.

7. For Electron SFs : 
> Copy all the SF files from 
#https://twiki.cern.ch/twiki/bin/view/CMS/EgammaRunIIRecommendations

> Update ElectronSFARC.py  to extract SF as event weights.
