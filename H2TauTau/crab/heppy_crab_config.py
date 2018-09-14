import os, imp, datetime
from CRABClient.UserUtilities import getUsernameFromSiteDB
from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'heppy_crab' +  "_" + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
config.General.workArea = 'heppy_crab_projects'
#config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'PrivateMC'#'Analysis'#
config.JobType.psetName = os.environ["CMSSW_BASE"]+'/src/CMGTools/H2TauTau/crab/heppy_crab_fake_pset.py'
config.JobType.scriptExe = os.environ["CMSSW_BASE"]+'/src/CMGTools/H2TauTau/crab/heppy_crab_script.sh'
#config.JobType.disableAutomaticOutputCollection = True

config.JobType.inputFiles = [
    os.environ["CMSSW_BASE"]+'/src/CMGTools/H2TauTau/crab/FrameworkJobReport.xml',
    os.environ["CMSSW_BASE"]+'/src/CMGTools/H2TauTau/crab/heppy_crab_script.py',
    'cmgdataset.tar.gz',
    'python.tar.gz',
    'cafpython.tar.gz',
    'options.json'
]
config.JobType.outputFiles = []
config.JobType.outputFiles.append("heppyOutput.tgz")

config.Data.inputDBS = 'global'
config.Data.splitting = 'EventBased'#'FileBased'#
config.Data.unitsPerJob = 1#0
#config.Data.totalUnits = config.Data.unitsPerJob * int(os.environ["NJOBS"])

config.Data.outLFNDirBase  = '/store/user/{username}/heppy_crab/{CMSSW_VERSION}/'.format(username=getUsernameFromSiteDB(), CMSSW_VERSION=os.environ["CMSSW_VERSION"])

config.Data.publication = False
config.Data.ignoreLocality = True

config.Site.storageSite = 'T3_FR_IPNL'
config.Site.whitelist = [
    'T3_FR_IPNL',
    # "T2_CH_CSCS", 
    # "T2_IT_Legnaro", 
    # "T2_UK_London_IC", 
    # "T2_UK_SGrid_Bristol", 
    # "T2_DE_DESY", 
    # "T2_ES_CIEMAT", 
    # "T2_IT_Rome", 
    # "T2_AT_Vienna",
    # "T2_DE_RWTH",
    # "T2_FR_GRIF_IRFU", 
    # "T2_HU_Budapest", 
    # "T2_FR_IPHC", 
    # "T2_BE_IIHE", 
    # "T2_IT_Pisa", 
    # "T2_ES_IFCA", 
    # "T2_UK_London_Brunel", 
    # "T2_US_Purdue", 
    # "T2_UA_KIPT", 
    # "T2_US_MIT", 
    # "T2_US_Wisconsin", 
    # "T2_US_UCSD", 
    # "T2_US_Vanderbilt", 
    # "T2_US_Caltech",
]

