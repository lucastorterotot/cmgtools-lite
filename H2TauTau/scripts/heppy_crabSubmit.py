#!/usr/bin/env python

from CMGTools.H2TauTau.tools.crab_utilities import load_base_config, ask_confirmation

if __name__ == '__main__':
    import os
    import sys
    import imp
    import pprint
    import json
    from optparse import OptionParser
    usage = '''usage: %prog [options] <heppy configuration file>
where <heppy configuration file> is the heppy input file also used locally.

Example of use: 

heppy_crabSubmit.py tauMu_2018_modular_cfg.py
'''
    parser = OptionParser(usage=usage)

    parser.add_option("-c", "--config", dest="config",
                      default = os.environ["CMSSW_BASE"]+'/src/CMGTools/H2TauTau/crab/heppy_crab_config.py',
                      help='base heppy crab configuration file. defaults to heppy_crab_config.py.')
    parser.add_option("-n", "--dry-run", dest="dryrun",
                      action='store_true',
                      default=False,
                      help='set up the jobs and do nothing')
    parser.add_option("-v", "--verbose", dest="verbose",
                      action='store_true',
                      default=False,
                      help='verbose mode')
    parser.add_option("-r", "--request_name", dest="request_name",
                      default=None,
                      help='base name for this request. default: <date_time>. The task name is built as <component_name>_<basename>.')
    
    options, args = parser.parse_args()

    if len(args)!=1:
        print parser.usage
        sys.exit(1)
    heppy_config = args[0]
  
    if options.dryrun:
        print 'Dry run, will do nothing'

    from PhysicsTools.HeppyCore.framework.heppy_loop import _heppyGlobalOptions
    from PhysicsTools.HeppyCore.framework.heppy_loop import split

    _heppyGlobalOptions["isCrab"] = True
    optjsonfile = open('options.json','w')
    optjsonfile.write(json.dumps(_heppyGlobalOptions))
    optjsonfile.close()

    print '----------------------------------------------------------------------'
    print 'Heppy outputs:'
    print ' '
    handle = open(heppy_config, 'r')
    cfo = imp.load_source(heppy_config.split('/')[-1].rstrip(".py"), heppy_config, handle)
    conf = cfo.config
    handle.close()
    print '----------------------------------------------------------------------'
    #print 'Ignore this number of jobs: not relevant for crab.'

    os.system("tar czf python.tar.gz --dereference --directory $CMSSW_BASE python")
    os.system("tar czf cmgdataset.tar.gz --directory $HOME .cmgdataset")
    os.system("tar czf cafpython.tar.gz --directory /afs/cern.ch/cms/caf/ python")

    print "Will send datasets:"
    for comp in conf.components:
        print "-", str(comp.name), "with", str(len(split([comp]))), "jobs"
        
    if options.dryrun:
        print 'Dry run, nothing happened.'
        
    if not options.dryrun:
        print 
        ask_confirmation()
        print 
        print 'Submitting heppy jobs based on', os.path.basename(heppy_config)
        for comp in conf.components:
            print "-", str(comp.name), "dataset with", str(len(split([comp]))), "jobs"
            os.environ["DATASET"] = str(comp.name)
            os.environ["NJOBS"] = str(len(split([comp])))
            os.environ["CFG_FILE"] = heppy_config
            os.system("crab submit %s -c {}".format(options.config)%("--dryrun" if options.dryrun else ""))
            #crabCommand('submit', config=options.config)
        
    os.system("rm options.json")
    os.system("rm python.tar.gz")
    os.system("rm cmgdataset.tar.gz")
    os.system("rm cafpython.tar.gz")
