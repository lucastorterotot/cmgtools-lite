#!/usr/bin/env python

from CRABAPI.RawCommand import crabCommand
from CRABClient.ClientExceptions import ClientException
from httplib import HTTPException

from CMGTools.H2TauTau.tools.crab_utilities import load_base_config, ask_confirmation, create_config

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
    parser.add_option("-e", "--nevents_per_job", dest="nevents_per_job",
                      default=int(5e4),
                      type='int',
                      help='desired approximate number of events per job. Defaults to 20k. Be aware that the larger the number of jobs, the more probable it is that your job is killed on the GRID because it is using too much memory. We do not advise values larger than 500k events.')
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

    print '______________________________________________________________________'
    print 
    print 'Heppy outputs:'
    print 
    handle = open(heppy_config, 'r')
    cfo = imp.load_source(heppy_config.split('/')[-1].rstrip(".py"), heppy_config, handle)
    conf = cfo.config
    handle.close()
    print '______________________________________________________________________'
    print 

    print 'Preparing python files...'
    os.system("tar czf python.tar.gz --dereference --directory $CMSSW_BASE python")
    print 'Preparing cmgdataset files...'
    os.system("tar czf cmgdataset.tar.gz --directory $HOME .cmgdataset")
    print 'Preparing cafpython files...'
    os.system("tar czf cafpython.tar.gz --directory /afs/cern.ch/cms/caf/ python")

    print 'Preparing configurations for components...'
    print

    selected_components = conf.components

    base_config = load_base_config(options.config)
    for component in selected_components:
        create_config(component, options, base_config, heppy_cfg=heppy_config)
        
    if not options.dryrun:
        print 
        ask_confirmation()

    if not options.dryrun:
        for component in selected_components:
            print 'submitting:'
            print component.dataset
            print component.config
            component_heppy_crab_submit_cfg_file_name = '_'.join([
                    'crab_submit_cfg', 
                    component.config.General.requestName
                    ])
            component_heppy_crab_submit_cfg_file_name += '.py'
            component_heppy_crab_submit_cfg_file = open(
                component_heppy_crab_submit_cfg_file_name,
                'w'
                )
            component_heppy_crab_submit_cfg_file.write(str(component.config))
            component_heppy_crab_submit_cfg_file.close()
            import pdb; pdb.set_trace()
            os.system("crab submit -c {}".format(
                    '/'.join([
                            os.getcwd(),
                            component_heppy_crab_submit_cfg_file_name
                            ])))
            #crabCommand('submit', config=component.config) # seems to be not able to submit heppy jobs
            os.system('rm ' + component_heppy_crab_submit_cfg_file_name.rstrip(".py") + '*')
    
    print 
    print 'All components submitted.'
    print 'Removing secondary submission files...'
    os.system("rm options.json")
    os.system("rm python.tar.gz")
    os.system("rm cmgdataset.tar.gz")
    os.system("rm cafpython.tar.gz")
    print 
    print 'Done.'
