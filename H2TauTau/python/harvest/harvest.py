import os
import shutil

from datasetdb import DatasetDB
from dataset import Dataset

def get_options():
     from optparse import OptionParser
     usage = "usage: %prog [options]"
     parser = OptionParser(usage=usage)
     parser.add_option("-d", "--dataset-pattern", dest="dataset_pattern",
                       default='*',
                       help='dataset pattern')
     parser.add_option("-n", "--negate", dest="negate",
                       action="store_true", default=False,
                       help='do nothing')
     (options,args) = parser.parse_args()
     if len(args)!=0:
          print parser.usage
          sys.exit(1)
     return options, args
     

class Harvester(object): 
     '''Harvests datasets
     Holds a connection to the database. 
     Manages harvesting for a collection of datasets
     '''

     def __init__(self, dataset_db):
          '''initialize the harvester with a connection to the db.
          dataset_db is of type datasetdb.DatasetDB
          '''
          self.dsdb = dataset_db

     
     def get_ds_infos(self, coll, regex): 
          '''returns infos for datasets with a name matching regex
          in collection coll
          '''
          return self.dsdb.find_by_name(coll, regex)


     def harvest(self, infos, destination): 
          '''harvest the datasets corresponding to infos
          the data is stored in the destination directory 
          IMPLEMENT MULTIPROCESSING MODE
          '''
          for info in infos: 
               self.harvest_one(info, destination)

     def harvest_one(self, info, destination):
          '''harvest one dataset'''
          self.fetch(info, destination)
     
     def fetch(self, info, destination, ntgzs=None):
          '''fetch the dataset and put it into a destination directory
          ntgzs : maximum number of tgzs to fetch. used for testing 
          '''
          ds = Dataset(info)
          basepath=os.getcwd()
          os.chdir(destination)
          destpath=os.getcwd()
          for subd, files in ds.info()['tgzs'].iteritems():
               print 'fetching subdir', subd
               os.mkdir(subd)
               os.chdir(subd)
               if ntgzs is None: 
                    ntgzs = len(files)
               for f in files[:ntgzs]:
                    path = ds.abspath('/'.join([subd, f]))
                    print path
                # print self.fhandler.ls(path)
                    ds.fhandler.cp(path, '.')
               os.chdir(destpath)
          os.chdir(basepath)
          return True



