import os
from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.transferLogs = True

config.section_("JobType")
config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = os.environ["CMSSW_BASE"]+'/src/CMGTools/H2TauTau/cfgPython/crab/heppy_crab_fake_pset.py'
config.JobType.scriptExe = os.environ["CMSSW_BASE"]+'/src/CMGTools/H2TauTau/cfgPython/crab/heppy_crab_script.sh'
config.JobType.disableAutomaticOutputCollection = True
# config.JobType.sendPythonFolder = True  #doesn't work, not supported yet? do it by hand

config.JobType.inputFiles = [
    os.environ["CMSSW_BASE"]+'/src/CMGTools/H2TauTau/cfgPython/crab/FrameworkJobReport.xml',
    os.environ["CMSSW_BASE"]+'/src/CMGTools/H2TauTau/cfgPython/crab/heppy_crab_script.py',
    'cmgdataset.tar.gz',
    'python.tar.gz',
    'cafpython.tar.gz',
    'options.json'
]
config.JobType.outputFiles = []

config.section_("Data")
config.Data.inputDBS = 'global'
config.Data.splitting = 'EventBased'
username = os.environ["USER"]
if username == 'torterotot':
    username = 'ltortero'
if username == 'touquet':
    username = 'gtouquet'
config.Data.outLFNDirBase = '/store/user/' + username
config.Data.publication = False

config.section_("Site")

