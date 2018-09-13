#!/usr/bin/env python

import imp 
import datetime
import copy
import sys
import os

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
    
def load_base_config(fname):
    '''Load crab config from file fname and return it'''
    config = None
    with open(fname) as ifile:
        mod = imp.load_source('mod', fname, ifile)
    config = mod.config
    return config

def create_config(component, options, base_config, heppy_cfg=None):
    '''create crab config for a given component'''
    config = copy.deepcopy(base_config)
    request_name = None
    if options.request_name:
        request_name = options.request_name
    else: 
        request_name = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    request_name = '_'.join([component.name,request_name])
    if heppy_cfg:
        config.JobType.inputFiles.append(heppy_cfg)
        request_name = '_'.join(['heppy',os.environ['CMSSW_VERSION'],request_name])
    else:
        config.Data.inputDataset = component.dataset
    config.General.requestName = request_name
    nfiles = len(component.files)
    config.Data.unitsPerJob=nfiles_per_job(options.nevents_per_job,
                                           component.dataset_entries,
                                           nfiles)
    if heppy_cfg:
        config.Data.totalUnits =  nfiles
        config.Data.outputDatasetTag = str(component.name)
        config.JobType.scriptArgs = ["dataset="+config.Data.outputDatasetTag, "total={}".format(nfiles), "useAAA=full", "cfgfile="+heppy_cfg.split('/')[-1]]
        config.Data.outputPrimaryDataset = os.path.basename(heppy_cfg).rstrip('.py')

    print 'Task:', 
    print '\t', component.dataset
    print '\tn evts(M) = {:5.2f}'.format(component.dataset_entries/1e6)
    print '\tn files   =', nfiles
    print '\tfiles/job =', config.Data.unitsPerJob
    print '\tn jobs    =', nfiles/config.Data.unitsPerJob
    if options.verbose: 
         print config
    component.config = config
