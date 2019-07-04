from datasetdb import DatasetDB
import pprint
from getpass import getpass 
import os
import pprint
import copy 

pwd = getpass()
dsdb = DatasetDB('writer', pwd, db='datasets')

infos = dsdb.find('se', {})

for info in infos: 
    tier_info = info.get('tiers', None)
    if not tier_info:
        continue
    info['harvesting'] = info['tiers']['harvesting']
    info['harvesting']['parent'] = None
    # del info['_id']
    del info['tiers']
    # pprint.pprint(info)
    dsdb.insert('se', info)
    # pprint.pprint(info)
