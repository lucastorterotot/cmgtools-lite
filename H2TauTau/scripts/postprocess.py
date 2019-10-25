#!/usr/bin/env python

from CMGTools.H2TauTau.harvest.datasetdb import DatasetDB
import CMGTools.H2TauTau.harvest.postproc as postproc
from getpass import getpass 

postproc.dataset_db = DatasetDB(mode='writer', pwd=getpass(), db='datasets')

def get_options():
     from optparse import OptionParser
     usage = "usage: %prog [options] <dest_dir> <tier> <new_tier> <script>"
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
     parser.add_option("-f", "--force", dest="force",
                       action="store_true", default=False,
                       help='force overwrite if processed dataset already exists')
     parser.add_option("-c", "--channel", dest="channel",
                       default='tt',
                       help='Channel: default is tt, but can be mt or et too.')
    
     (options,args) = parser.parse_args()
     if len(args)!=4:
          print parser.usage
          sys.exit(1)
     return options, args
     

if __name__ == '__main__':
     
     import pprint 
     import sys 

     options, args = get_options()
     destdir, tier, new_tier, script = args
     sel, done, skip = postproc.get_datasets(options.dataset_pattern, tier, new_tier)
     if options.force: 
          sel.extend(done)
     for name in sorted(info['name'] for info in sel):
          print(name)
     nworkers = min(len(sel), options.workers)
     print('{} -> {}'.format(tier, new_tier))
     print('{} datasets to be processed on {} workers. {} done, {} skipped'.format(
               len(sel), 
               nworkers, 
               len(done), len(skip))
           )
     if options.negate or not len(sel):
          sys.exit(0)

     choice = 'foobar'
     while choice not in 'yn': 
          choice = raw_input('are you sure? [y/n]')
     if choice == 'n':
          print('operation cancelled')
          sys.exit(0)

     postproc.process(sel, 
                      tier, 
                      script,
                      destdir,
                      new_tier,
                      nworkers=nworkers,
                      delete='n',
                      channel=options.channel)
