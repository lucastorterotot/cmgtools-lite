from datasetdb import DatasetDB
import pprint
from getpass import getpass 
import os
import pprint
import copy 

pwd = getpass()
dsdb = DatasetDB('reader', pwd, db='datasets')
infos = dsdb.find('se', {'path':{'$exists':1}})

for info in infos:
    tgzs = info['tgzs']
    htgzs = info['tiers']['harvesting']['tgzs']
    if cmp(tgzs, htgzs) != 0: 
        pprint.pprint(tgzs)
        pprint.pprint(htgzs)
        assert(False)
