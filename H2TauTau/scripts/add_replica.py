

from getpass import getpass 

def get_options():
     from optparse import OptionParser
     usage = """usage: %prog [options] <tier> <path>

Record in the database that this tier has been replicated to path.
path should be of the form:  
   machine_address:absolute_path

Before running this script, make sure to copy the tier with rsync in this way: 


"""
     parser = OptionParser(usage=usage)
     parser.add_option("-p", "--dataset-pattern", dest="dataset_pattern",
                       default='.*',
                       help='dataset regex pattern')
     parser.add_option("-n", "--negate", dest="negate",
                       action="store_true", default=False,
                       help='do nothing')
     (options,args) = parser.parse_args()
     if len(args)!=2:
          print parser.usage
          sys.exit(1)
     return options, args
     

if __name__ == '__main__':
     
     import pprint 
     import sys 
     import copy
     import time
     from CMGTools.H2TauTau.harvest.datasetdb import DatasetDB

     options, args = get_options()
     tier, path = args

     dsdb = DatasetDB(mode='writer', pwd=getpass(), db='datasets')
     infos = list(dsdb.db['se'].find({'name': {'$regex':options.dataset_pattern}, 
                                      tier: {'$exists':1}}))
     for info in infos: 
          print(info['name'])
     print('{} datasets will be affected'.format(len(infos)) )

     machine, directory = path.split(':')
     timestamp = time.time()
     new_tier_info = { machine : { 'dir' : directory,
                                   'time': timestamp, 
                                   }
                       }
                       
     print('\nold info')
     pprint.pprint(infos[0][tier])
     print('\nnew info')
     new_info = copy.deepcopy(infos[0])
     new_info[tier].setdefault('replicas', {}).update(new_tier_info)
     pprint.pprint(new_info[tier])

     if options.negate or not len(infos):
          sys.exit(0)

     choice = 'foobar'
     while choice not in 'yn': 
          choice = raw_input('are you sure? [y/n]')
     if choice == 'n':
          print('operation cancelled')
          sys.exit(0)

     for info in infos: 
          new_info = copy.deepcopy(info)
          new_info[tier].setdefault('replicas', {}).update(new_tier_info)
          dsdb.insert('se', new_info)

