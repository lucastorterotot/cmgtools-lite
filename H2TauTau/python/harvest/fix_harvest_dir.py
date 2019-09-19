from datasetdb import DatasetDB
import pprint
from getpass import getpass 
import os
import pprint
import copy 

pwd = getpass()
dsdb = DatasetDB('writer', pwd, db='datasets')

infos = dsdb.find('se', {'harvesting':{'$exists':1}})

for info in infos: 
    dirname = info['harvesting']['dir'] 
    if '%' not in dirname: 
        continue
    newdirname = os.path.dirname(dirname)
    print(dirname)
    print(newdirname)
    info['harvesting']['dir'] = newdirname
    dsdb.insert('se', info)

