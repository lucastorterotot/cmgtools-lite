from datasetdb import DatasetDB
import pprint
from getpass import getpass 
import os
import pprint
import copy 

pwd = getpass()
dsdb = DatasetDB('writer', pwd, db='datasets')
hinfos = dsdb.find('harvested', {})

for hinfo in hinfos: 
    harvdir = hinfo['harv_dir']
    basedir = os.path.dirname(harvdir)
    # print(basedir)
    infos = dsdb.find('se', {'name':hinfo['name']})
    assert(len(infos) == 1)
    info = infos[0]
    tier_info = {
        'dir'  : basedir, 
        'time' : hinfo['harv_time'],
        'tgzs'  : hinfo['tgzs'], 
        }
    # pprint.pprint(tier_info)
    info.setdefault('tiers', {})['harvesting'] = tier_info
    del info['tiers']
    # dsdb.insert('se', info)
    # pprint.pprint(info)
