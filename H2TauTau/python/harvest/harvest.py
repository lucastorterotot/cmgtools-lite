import os
import shutil
import tempfile 
import time

from dataset import Dataset
from multiprocessing import Pool

# to be set by user
datasetdb = None

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
     
def wait_a_bit(nsec):
     time.sleep(nsec)
     print('done')


def harvest_one(info, destination, ntgzs=None):
     '''harvest one dataset
     
     dataset is: 
     - fetched
     - unpacked
     - hadded 
     - copied to destination on lyovis10 (don't forget the tunnel)
     
     Finally, its info is added to the harv table in the db
     '''
     print('there')
     tmpdir = tempfile.mkdtemp()
     fetch(info, tmpdir, ntgzs)
     unpack(info, tmpdir, ntgzs)
     hadd(tmpdir)
     sampledir = '/'.join([tmpdir,info['name']])
     # print(sampledir)
     scp(sampledir, 'localhost:'+destination, '-P 2222')
     shutil.rmtree(tmpdir)
     del info['_id']
     info['harv_time'] = time.time()
     info['harv_dir'] = sampledir
     return info 

def get_ds_infos(coll, regex): 
     '''returns infos for datasets with a name matching regex
     in collection coll
     '''
     return datasetdb.find_by_name(coll, regex)


def harvest(infos, destination, nworkers=None, ntgzs=None): 
     '''harvest the datasets corresponding to infos
     the data is stored in the destination directory 
     IMPLEMENT MULTIPROCESSING MODE
     '''
     hinfos = []
     if nworkers is None or nworkers==1:
          for info in infos: 
               hinfos.append(harvest_one(info, destination, ntgzs))
     else: 
          p = Pool(nworkers)
          futures = []
          for info in infos: 
               futures.append( p.apply_async( harvest_one, 
                                              (info, destination, ntgzs)) )
          for future in futures: 
               hinfos.append(future.get())
          print('here')
          p.close()
          p.join()
     for hinfo in hinfos: 
          datasetdb.insert('harvested', hinfo)


def fetch(info, destination, ntgzs=None):
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
               ds.fhandler.cp(path, '.')
          os.chdir(destpath)
     os.chdir(basepath)
     return True


def scp(directory, destination, options=''): 
     '''scp the directory to a destination'''
     cmd = 'scp -r {} {} {}'.format(
          options, directory, destination
          )
     os.system(cmd)


def hadd(directory):
     '''Run heppy_hadd in directory, 
     and remove the chunks'''
     oldpath=os.getcwd()
     os.chdir(directory)
     os.system('heppy_hadd.py .')
     os.system('rm -rf *Chunk*')
     os.chdir(oldpath)


def unpack(info, destination, ntgzs=None):
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
          
