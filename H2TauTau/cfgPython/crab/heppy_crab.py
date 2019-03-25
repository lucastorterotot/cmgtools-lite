#!/usr/bin/env python
import imp
import os 
import json
import sys
from optparse import OptionParser,OptionGroup

### auto-monitoring tool
os.system("python crabMonitoring.py 0")

parser = OptionParser(usage = 'heppy_crab.py [options] <heppy configuration file>')

g1 = OptionGroup(parser,"Heppy options")
# g1.add_option("-c", "--cfg-file", dest="cfg_file", 
#               help="heppy .cfg file to use", default="myHeppyCrabProdDummy")
g1.add_option("-o", "--option", dest="extraOptions", 
              type="string", action="append", default=[], 
              help="heppy options to use for task preparation and in remote jobs (the isCrab option is automatically set, can be used in the .cfg to configure it for running on crab)")
g1.add_option("--AAAconfig", dest="AAAconfig", 
              default="full", 
              help="AAA configuration: full (free AAA access via redirector), local (force reading from local site, will turn AAA and ignoreLocality off), eos (force reading from EOS via AAA)")
parser.add_option_group(g1)

g2 = OptionGroup(parser,"Stageout options")
g2.add_option("-s", "--storage-site", dest="storageSite", 
              default='T3_FR_IPNL',
              help="site where the output should be staged out (T2_XX_YYYY)")
g2.add_option("-d", "--output-dir", dest="outputDir", 
              help="name of the directory where files will be staged out: /store/user/$USER/<output_dir>/<cmg_version>/<production_label>/dataset/$date_$time/0000/foo.bar", default="heppyTrees")
g2.add_option("-l", "--production-label", dest="production_label", 
              help="heppy_crab production label", default=None)
g2.add_option("-v", "--cmg-version", dest="cmg_version", 
              help="CMGTools version used", default=os.environ['CMSSW_VERSION'])
g2.add_option("-u", "--unpackFile", dest="filesToUnpack", 
              type="string", action="append", default=[], 
              help="Files to unpack when staging out (relative to output directory)")
parser.add_option_group(g2)
g2.add_option("--only-unpacked", dest="only_unpacked", 
              default=False, action="store_true", 
              help="Only return the unpacked files, not the whole compressed output directory")

parser.add_option("-n", "--dryrun", dest="dryrun", action="store_true",default=False, help="dryrun")
parser.add_option("-w", "--siteWhitelist", dest="siteWhitelist", type="string", 
                  action="append", default=[], 
                  help="Sites whitelist (default is using the one in heppy_crab_config.py)")
parser.add_option("-b", "--siteBlacklist", dest="siteBlacklist", type="string", 
                  action="append", default=[], 
                  help="Sites blacklist (default is using the one in heppy_crab_config.py)")
parser.add_option("-N", dest="maxevents", default=-1, 
                  help="maximum number of events to process per heppy run (for debugging purposes)")
parser.add_option("--ship-file", dest='filesToShip', 
                  default=[], action="append", type="string", 
                  help="additional files to ship to WN (will be placed in the same directory as the .cfg when running)")

(options,args) = parser.parse_args()

if len(args)!=1:
    print parser.usage
    sys.exit(1)
heppy_config = args[0]

if options.production_label is None:
    options.production_label = os.path.basename(heppy_config).rstrip('.py')


# datasets to run as defined from cfg file
# number of jobs to run per dataset decided based on splitFactor and fineSplitFactor from cfg file

from PhysicsTools.HeppyCore.framework.heppy_loop import _heppyGlobalOptions
from PhysicsTools.HeppyCore.framework.heppy_loop import split

for opt in options.extraOptions:
    if "=" in opt:
        (key,val) = opt.split("=",1)
        _heppyGlobalOptions[key] = val
    else:
        _heppyGlobalOptions[opt] = True
_heppyGlobalOptions["isCrab"] = True
optjsonfile = open('options.json','w')
optjsonfile.write(json.dumps(_heppyGlobalOptions))
optjsonfile.close()

handle = open(heppy_config, 'r')
cfo = imp.load_source(heppy_config.split('/')[-1].rstrip(".py"), heppy_config, handle)
if hasattr(cfo,'configs'):
    confs = cfo.configs
else:
    confs = {'nominal':cfo.config}
handle.close()

os.system("tar czf python.tar.gz --dereference --directory $CMSSW_BASE python")
os.system("tar czf cmgdataset.tar.gz --directory $HOME .cmgdataset")
os.system("tar czf cafpython.tar.gz --directory /afs/cern.ch/cms/caf/ python")

os.environ["PROD_LABEL"]  = options.production_label
os.environ["CMG_VERSION"] = options.cmg_version
os.environ["USEAAA"]      = options.AAAconfig
os.environ["STAGEOUTREMDIR"] = options.outputDir
os.environ["CFG_FILE"] = heppy_config
os.environ["OUTSITE"] = options.storageSite
if len(options.siteWhitelist)>0: os.environ["WHITESITES"] = ','.join(options.siteWhitelist)
if len(options.siteBlacklist)>0: os.environ["BLACKSITES"] = ','.join(options.siteBlacklist)
if len(options.filesToUnpack)>0: os.environ["FILESTOUNPACK"] = ','.join(options.filesToUnpack)
if len(options.filesToShip)>0: os.environ["FILESTOSHIP"] = ','.join(options.filesToShip)
if options.maxevents>0: os.environ["MAXNUMEVENTS"] = str(options.maxevents)
os.environ["ONLYUNPACKED"] = str(options.only_unpacked)

for confname, conf in confs.iteritems():
    for comp in conf.components:
        if getattr(comp,"useAAA",False):
            raise RuntimeError, 'Components should have useAAA disabled in the cfg when running on crab. \
Tune the behaviour of AAA in the crab submission instead!'
        os.environ["PROD_LABEL"]  = '{}_{}'.format(options.production_label, confname)
        os.environ["DATASET"] = str(comp.name)
        os.environ["CFG_NAME"] = confname
        os.environ["NJOBS"] = str(len(split([comp])))
        os.system("crab submit %s -c heppy_crab_config_env.py"%("--dryrun" if options.dryrun else ""))

os.system("rm options.json")
os.system("rm python.tar.gz")
os.system("rm cmgdataset.tar.gz")
os.system("rm cafpython.tar.gz")
