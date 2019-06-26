
from CMGTools.H2TauTau.harvest.datasetdb import DatasetDB

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

     def get_ds_info(self, pattern): 
          pass 
