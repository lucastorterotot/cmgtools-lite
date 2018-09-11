#!/usr/bin/env python

from CMGTools.H2TauTau.proto.samples.component_index import ComponentIndex

from CRABAPI.RawCommand import crabCommand
from CRABClient.ClientExceptions import ClientException
from httplib import HTTPException

from CMGTools.H2TauTau.tools.crab_utilities import load_base_config, ask_confirmation, nfiles_per_job, create_config
    
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

if __name__ == '__main__':
    import os
    import sys
    import imp
    import pprint
    from optparse import OptionParser
    usage = '''usage: %prog [options] pattern

pattern can be either:
- a wildcard pattern, e.g. '/DYJets*'. Note the quotes around the pattern, necessary to avoid the pattern to be interpreted by the shell.
- a set of wildcard patterns separated by commas, e.g. '/DYJets*,*BB*'
- a file with a pattern on each line, e.g. file.txt:

/DYJets*
/WJets*
*Higgs*

Example of use: 

./crabSubmit.py '*BB1000*' -r version2 -e 10000
'''
    parser = OptionParser(usage=usage)

    default_module = os.path.expandvars('$CMSSW_BASE/src/CMGTools/H2TauTau/python/proto/samples/summer16/htt_common.py')
    parser.add_option("-c", "--config", dest="config",
                      default='crabConfig.py',
                      help='base crab configuration file. defaults to crabConfig.py.')
    parser.add_option("-m", "--module", dest="module",
                      default=default_module,
                      help='module where the components are defined. Defaults to '+default_module)
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
                      help='base name for this request. default: <date_time>. The task name is built as <component_name>_<basename>. For the example above, the task name is therefore: HiggsSUSYBB1000_version2')
    
    options, args = parser.parse_args()

    if len(args)!=1:
        print parser.usage
        sys.exit(1)
    pattern = args[0]
  
    if options.dryrun:
        print 'Dry run, will do nothing'

    if not options.dryrun:
        maxeventsperjob = int(2e5)
        if options.nevents_per_job > maxeventsperjob:
            print 'More than {} events/job requested ({})'.format(maxeventsperjob,
                                                                  options.nevents_per_job)
            ask_confirmation()
            

    index=ComponentIndex(options.module)
    
    selected_components=get_selected_components(pattern)
    if len(selected_components)==0:
        print 'No dataset matches pattern', pattern
        sys.exit(2)
#    print 'datasets to be submitted:'
#    pprint.pprint(index.glob(pattern))

    base_config = load_base_config(options.config)
    for component in selected_components:
        create_config(component, options, base_config)
        
    if not options.dryrun:
        print 
        ask_confirmation()

    if not options.dryrun:
        for component in selected_components:
            print 'submitting:'
            print component.dataset
            print component.config
            import pdb; pdb.set_trace()
            crabCommand('submit', config=component.config)
        
    
