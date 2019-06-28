from datasetdb import DatasetDB
import pprint

dsdb = DatasetDB(mode='writer', db='datasets')
infos = dsdb.find('harvested', {})

basedir = '/gridgroup/cms/cbernet/test/'
for info in infos: 
    name = info['harv_dir'].split('/')[-1]
    harvdir = basedir + name
    del info['_id']
    info['harv_dir'] = harvdir
    dsdb.insert('harvested', info)
