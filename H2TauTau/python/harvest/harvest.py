import os
import shutil
import tempfile 
import time

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

     def harvest_one(self, info, destination, ntgzs=None):
          '''harvest one dataset
          
          dataset is: 
          - fetched
          - unpacked
          - hadded 
          - copied to destination on lyovis10 (don't forget the tunnel)
          
          Finally, its info is added to the harv table in the db
          '''
          tmpdir = tempfile.mkdtemp()
          self.fetch(info, tmpdir, ntgzs)
          self.unpack(info, tmpdir, ntgzs)
          self.hadd(tmpdir)
          sampledir = '/'.join([tmpdir,info['name']])
          # print(sampledir)
          self.scp(sampledir, 'localhost:'+destination, '-P 2222')
          shutil.rmtree(tmpdir)
          del info['_id']
          info['harv_time'] = time.time()
          info['harv_dir'] = sampledir
          self.dsdb.insert('harvested', info)

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


     def scp(self, directory, destination, options=''): 
          '''scp the directory to a destination'''
          cmd = 'scp -r {} {} {}'.format(
               options, directory, destination
               )
          os.system(cmd)

     def hadd(self, directory):
          '''Run heppy_hadd in directory, 
          and remove the chunks'''
          oldpath=os.getcwd()
          os.chdir(directory)
          os.system('heppy_hadd.py .')
          os.system('rm -rf *Chunk*')
          os.chdir(oldpath)

     def unpack(self, info, destination, ntgzs=None):
          '''unpacks the dataset after fetching. 
          each tgz file is unpacked into an heppy chunk, 
          for later heppy_hadd
          '''
          oldpath=os.getcwd()
          os.chdir(destination)
          destpath = os.getcwd()
          chunks = dict()
          for subd, tgzs in info['tgzs'].iteritems():
               # print 'unpacking subdir', subd
               subdid = int(subd)
               os.chdir(subd)
               chunks[subd] = []
               if ntgzs is None:
                    ntgzs = len(tgzs)
               for tgz in tgzs[:ntgzs]: 
                    print 'unpacking', tgz
                    os.system('tar -zxf {}'.format(tgz))
                    # tgz is e.g. heppyOutput_43.tgz
                    # so index is 43
                    index = int(os.path.splitext(tgz)[0].split('_')[1]) + subdid
                    chunkname = '{}_Chunk{}'.format(info['name'], index)
                    chunks[subd].append(chunkname)
                    os.rename('Output', '../'+chunkname)
                    os.remove(tgz)
               os.chdir(destpath)
               shutil.rmtree(subd)
          os.chdir(oldpath)
          
