#!/usr/bin/env python

from CMGTools.H2TauTau.proto.samples.component_index import ComponentIndex

from CRABAPI.RawCommand import crabCommand
from CRABClient.ClientExceptions import ClientException
from httplib import HTTPException

import imp 
import datetime
import copy

def ask_confirmation():
    '''ask user confirmation for submission and exit if no'''
    answer = None
    while answer not in ['y','n']:
        answer=raw_input('Confirm submission? [y/n]')
    if answer == 'n':
        print 'submission cancelled.'
        sys.exit(3)
    

def nfiles_per_job(nevents_per_job, nevents, nfiles):
    '''Compute the number of files / job'''
    nevents_per_file=nevents/nfiles
    nfiles_per_job = nevents_per_job/nevents_per_file
    if nfiles_per_job == 0: 
        nfiles_per_job+=1
    return nfiles_per_job
    
def get_selected_components(pattern_or_fname):
    '''Returns the list of components matching pattern_or_fname.
    pattern_or_fname can be: 
    - a wildcard pattern
    - a comma-separated list of patterns
    - the path to a file containing on each line a pattern
    '''
    if os.path.isfile(pattern_or_fname):
        sys.exit(4)
    patterns = pattern_or_fname.split(',')
    selected=[]
    for pattern in patterns:
        selected.extend(index.glob(pattern))
    return selected
    
def load_base_config(fname):
    '''Load crab config from file fname and return it'''
    config = None
    with open(fname) as ifile:
        mod = imp.load_source('mod', fname, ifile)
    config = mod.config
    return config

def create_config(component, options, base_config):
    '''create crab config for a given component'''
    config = copy.deepcopy(base_config)
    request_name = None
    if options.request_name:
        request_name = options.request_name
    else: 
        request_name = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    request_name = '_'.join([component.name,request_name])
    config.General.requestName = request_name
    config.Data.inputDataset = component.dataset
    nfiles = len(component.files)
    config.Data.unitsPerJob=nfiles_per_job(options.nevents_per_job,
                                           component.dataset_entries,
                                           nfiles)
    print 'Task:', 
    print '\t', component.dataset
    print '\tn evts(M) = {:5.2f}'.format(component.dataset_entries/1e6)
    print '\tn files   =', nfiles
    print '\tfiles/job =', config.Data.unitsPerJob
    print '\tn jobs    =', nfiles/config.Data.unitsPerJob
    if options.verbose: 
         print config
    component.config = config


if __name__ == '__main__':
    import os
    import sys
    import imp
    import pprint
    import json
    from optparse import OptionParser,OptionGroup
    usage = '''usage: %prog [options] <heppy configuration file>
where <heppy configuration file> is the heppy input file also used locally.

Example of use: 

heppy_crabSubmit.py ../mt/tauMu_2018_modular_cfg.py
'''
    parser = OptionParser(usage=usage)

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
                      action="append", default=['T3_FR_IPNL'], 
                      help="Sites whitelist (default is using the one in heppy_crab_config.py)")
    parser.add_option("-N", dest="maxevents", default=-1, 
                      help="maximum number of events to process per heppy run (for debugging purposes)")
    parser.add_option("--ship-file", dest='filesToShip', 
                      default=[], action="append", type="string", 
                      help="additional files to ship to WN (will be placed in the same directory as the .cfg when running)")
    
    options, args = parser.parse_args()

    if len(args)!=1:
        print parser.usage
        sys.exit(1)
    heppy_config = args[0]

    if options.production_label is None:
        options.production_label = os.path.basename(heppy_config).rstrip('.py')
  
    if options.dryrun:
        print 'Dry run, will do nothing'

    #TODO : following lines relevant?
    # if not options.dryrun:
    #     maxeventsperjob = int(2e5)
    #     if options.nevents_per_job > maxeventsperjob:
    #         print 'More than {} events/job requested ({})'.format(maxeventsperjob,
    #                                                               options.nevents_per_job)
    #         ask_confirmation()



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

    print 'Heppy outputs:'
    handle = open(heppy_config, 'r')
    cfo = imp.load_source(heppy_config.split('/')[-1].rstrip(".py"), heppy_config, handle)
    conf = cfo.config
    handle.close()
    print 'Ignore this number of jobs: used only if heppy run locally.'

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
    if len(options.filesToUnpack)>0: os.environ["FILESTOUNPACK"] = ','.join(options.filesToUnpack)
    if len(options.filesToShip)>0: os.environ["FILESTOSHIP"] = ','.join(options.filesToShip)
    if options.maxevents>0: os.environ["MAXNUMEVENTS"] = str(options.maxevents)
    os.environ["ONLYUNPACKED"] = str(options.only_unpacked)

    for comp in conf.components:
        if getattr(comp,"useAAA",False):
            raise RuntimeError, 'Components should have useAAA disabled in the cfg when running on crab. \
Tune the behaviour of AAA in the crab submission instead!'
        os.environ["DATASET"] = str(comp.name)
        os.environ["NJOBS"] = str(len(split([comp])))
        os.system("crab submit %s -c $CMSSW_BASE/src/CMGTools/H2TauTau/cfgPython/crab/heppy_crab_config_env.py"%("--dryrun" if options.dryrun else ""))

    os.system("rm options.json")
    os.system("rm python.tar.gz")
    os.system("rm cmgdataset.tar.gz")
    os.system("rm cafpython.tar.gz")
