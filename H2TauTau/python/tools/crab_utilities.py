#!/usr/bin/env python

from CMGTools.H2TauTau.proto.samples.component_index import ComponentIndex

from CRABAPI.RawCommand import crabCommand
from CRABClient.ClientExceptions import ClientException
from httplib import HTTPException

import imp 
import datetime
import copy
import sys

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
