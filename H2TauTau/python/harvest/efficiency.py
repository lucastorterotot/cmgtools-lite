from datasetdb import DatasetDB
from getpass import getpass

pwd = getpass()
dsdb = DatasetDB('reader', pwd, db='datasets')

def get_nchunks(info):
    tgzs = info.get('tgzs', None)
    if tgzs is None: 
        return 0
    nchunks = 0
    for subd, subdchunks in tgzs.iteritems(): 
        nchunks += len(subdchunks) 
    return nchunks

def efficiency(name): 
    infos = dsdb.find('se', {'name':name})
    if not infos: 
        raise ValueError(name + ' not found in the database')
    info = infos[0]
    nchunks = get_nchunks(info)
    njobs = info['njobs']
    if njobs is None: 
        njobs = 99
    return float(nchunks)/njobs
