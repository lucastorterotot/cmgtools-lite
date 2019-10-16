'''Tools for parallel post-processing of the datasets'''

import os
import imp 
import shutil
import copy
from multiprocessing import Pool

dataset_db = None

def get_datasets(dataset_regex, tier, new_tier): 
    '''returns infos from the database for datasets containing 
    dataset_regex
    '''
    if not dataset_db: 
        raise ValueError('first set postproc.dataset_db to a valid DatasetDB object')
    infos = dataset_db.find_by_name('se', dataset_regex)
    selected = []
    done = []
    skipped = []
    for info in infos: 
        if new_tier in info: 
            # done
            done.append(info)
        elif tier not in info:
            # cannot do the processing
            skipped.append(info)
        else: 
            # will do! 
            selected.append(info)
    return selected, done, skipped


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


def process(infos, tier, script, destination, new_tier, nworkers=None, delete='ask', channel='tt'):
    '''process all datasets with the process function in the script module
    '''
    if os.path.isdir(destination):
        while delete not in 'yne': 
            delete = raw_input('{} exists. remove it? [y(es)/n(o)/e(exit)]'.format(destination))
        if delete == 'y':
            shutil.rmtree(destination)
            os.mkdir(destination)
        elif delete == 'e': 
            sys.exit(0)
        else: # we keep the directory to add inside
            pass
    else:
        os.mkdir(destination)
    func, meta = load_script(script)
    if 'channel' in meta:
        meta['channel'] = channel
    new_infos = []
    if nworkers is None or nworkers==1:
        for info in infos: 
            new_infos.append(process_dataset(info, tier, func, meta, 
                                             destination, new_tier))
    else:
        print('work starting on {} workers, please be patient...'.format(nworkers) )
        p = Pool(nworkers)
        futures = []
        for info in infos: 
            futures.append( p.apply_async( process_dataset, 
                                           (info, tier, func, meta,
                                            destination, new_tier)) )
        for future in futures: 
            new_infos.append(future.get())
        p.close()
        p.join()
    for info in new_infos: 
        dataset_db.insert('se', info)

