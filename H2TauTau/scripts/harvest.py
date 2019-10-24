#!/usr/bin/env python

from CMGTools.H2TauTau.harvest.datasetdb import DatasetDB
import CMGTools.H2TauTau.harvest.harvest as harvest
from getpass import getpass 

harvest.datasetdb = DatasetDB(mode='writer', pwd=getpass(), db='datasets')

def get_options():
     from optparse import OptionParser
     usage = "usage: %prog [options] <dest_dir>"
     parser = OptionParser(usage=usage)
     parser.add_option("-p", "--dataset-pattern", dest="dataset_pattern",
                       default='.*',
                       help='dataset regex pattern')
     parser.add_option("-n", "--negate", dest="negate",
                       action="store_true", default=False,
                       help='do nothing')
     parser.add_option("-w", "--workers", dest='workers', 
                       default = 20, 
                       type='int',
                       help='number of workers. default 20')
     parser.add_option("-v", "--verbose", dest="verbose",
                       action="store_true", default=False,
                       help='verbose printout')
    
     (options,args) = parser.parse_args()
     if len(args)!=1:
          print parser.usage
          sys.exit(1)
     return options, args
     

if __name__ == '__main__':
     
     import pprint 
     import sys 

     options, args = get_options()
     destdir = args[0]
     infos,done = harvest.get_ds_infos(options.dataset_pattern)
     for name in sorted(info['name'] for info in infos):
          print(name)
     print('{} datasets to be harvested, {} skipped.  {} workers'.format(
               len(infos),
               len(done),
               options.workers)
           )
     if len(infos):
          estimated_time = len(infos)*30./options.workers/3600.
          print('estimated time: {:3.1f} hours'.format(estimated_time))
     if options.negate or not len(infos):
          sys.exit(0)

     choice = 'foobar'
     while choice not in 'yn': 
          choice = raw_input('are you sure? [y/n]')
     if choice == 'n':
          print('operation cancelled')
          sys.exit(0)

     harvest.harvest(infos, destdir, nworkers=options.workers)
