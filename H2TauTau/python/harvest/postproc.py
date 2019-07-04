'''Tools for parallel post-processing of the datasets'''

import os
import imp 
import shutil
import copy

dataset_db = None

def get_datasets(dataset_regex): 
    '''returns infos from the database for datasets containing 
    dataset_regex
    '''
    if not dataset_db: 
        raise ValueError('first set postproc.dataset_db to a valid DatasetDB object')
    return dataset_db.find_by_name('se', dataset_regex)


def load_script(script):
    '''loads the script, and returns: 
    - the process function
    - the meta information dictionary
    '''
    with open(script) as source:
        mod = imp.load_source('mod', script, source)
        return mod.process, mod.meta


def prepare_output_dataset(source, destination): 
    '''prepare output dataset directory structure.
    no root file is copied, and the root file created by the processing is added later
    '''
    oldcwd = os.getcwd()
    adest = os.path.abspath(destination)
    if os.path.isdir(adest): 
        shutil.rmtree(adest)
    os.mkdir(adest)
    os.chdir(source)
    for root, dirs, files in os.walk('.'):
        if root=='.':
            continue
        droot = os.path.join(adest, root)
        os.mkdir( droot )
        for f in files: 
            if not f.endswith('.root'): 
                shutil.copyfile(os.path.join(root,f), 
                                os.path.join(droot,f))
    os.chdir(oldcwd)


def process_dataset(info, tier, func, meta, destination, new_tier):
    '''process a single dataset'''
    adestination = os.path.abspath(destination)
    sourcedir = info[tier]['dir']
    sourceds = os.path.join(sourcedir, info['name'])
    destds = os.path.join(destination, info['name'])
    prepare_output_dataset(sourceds, destds)
    oldwd = os.getcwd()

    # move to the root of the output dataset
    os.chdir(destds)
 
    # do work
    ofname, path_in_dataset = func(sourceds) 
    shutil.move(ofname, path_in_dataset)

    # prepare new tier info
    tier_info = copy.deepcopy(meta)
    tier_info['dir'] = adestination
    tier_info['parent'] = tier

    new_info = copy.deepcopy(info)
    new_info[new_tier] = tier_info

    # come back
    os.chdir(oldwd)
    return new_info


def process(dataset_regex, tier, script, destination, new_tier):
    '''process all datasets with a name containg the dataset_regex
    regex pattern, with the process function in the script module
    '''
    infos = get_datasets(dataset_regex)
    print(len(infos))
    func, meta = load_script(script)
    for info in infos: 
        pprint.pprint(info)
        process_dataset(info, tier, func, meta, destination, new_tier) 
        
