'''Harvesting tools

set 
harvest.datasetdb 
before using 
See datasetdb.py for more information
'''

import os
import shutil
import tempfile 
import time

from dataset import Dataset
from multiprocessing import Pool

# to be set by user
datasetdb = None

def harvest_one(info, destination, ntgzs=None):
     '''harvest one dataset
     
     dataset is: 
     - fetched
     - unpacked
     - hadded 
     - copied to a destination directory 
     
     returns info for the harvested dataset, 
     including harv_time and harv_dir
     '''
     print('there')
     tmpdir = tempfile.mkdtemp()
     fetch(info, tmpdir, ntgzs)
     unpack_exit_code = unpack(info, tmpdir, ntgzs)
     hadd(tmpdir)
     tmpsampledir = '/'.join([tmpdir,info['name']])
     destsampledir = '/'.join([destination, info['name']])
     if os.path.isdir(destsampledir): 
          shutil.rmtree(destsampledir)
     shutil.move(tmpsampledir, destsampledir)
     shutil.rmtree(tmpdir)
     if not unpack_exit_code == 0:
          return info 
     del info['_id']
     harv_info = {
          'time': time.time(),
          'parent': None, 
          'dir': destination, 
          'tgzs': info['tgzs']
          }
     info['harvesting'] = harv_info
     return info 

def get_ds_infos(regex): 
     '''returns infos for datasets with a name matching regex
     in collection coll, and with a path on the SE so that they can be harvested
     '''
     infos = datasetdb.find_by_name('se', regex)
     selected = []
     done = []
     for info in infos: 
          if 'path' not in info: 
               continue          
          do_harvest = False
          hinfo = info.get('harvesting', None)
          if hinfo is None: 
               do_harvest = True
          else: 
               for subd, tgzs in info['tgzs'].iteritems(): 
                    if (subd not in hinfo['tgzs']) or \
                             len(tgzs) > len(hinfo['tgzs'][subd]):
                         # subdir was not harvested yet, 
                         # or subdir contains addtl tgzs
                         do_harvest = True
          if do_harvest: 
               selected.append(info) 
          else: 
               done.append(info)
     return selected, done

def harvest(infos, destination, nworkers=None, ntgzs=None, delete='ask'): 
     '''harvest the datasets corresponding to infos
     the data is stored in the destination directory 
     '''
     if os.path.isdir(destination):
          while delete not in 'yne': 
               delete = raw_input('{} exists. remove it? [y(es)/n(o)/e(exit)]'.format(destination))
          if delete == 'y':
               shutil.rmtree(destination)
               os.mkdir(destination)
          elif delete == 'e': 
               sys.exit(0)
          else: # we keep the directory to add inside
               pass
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
          datasetdb.insert('se', hinfo)


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
     untar_exit_code_sum = 0
     for subd, tgzs in info['tgzs'].iteritems():
          # print 'unpacking subdir', subd
          subdid = int(subd)
          os.chdir(subd)
          chunks[subd] = []
          if ntgzs is None:
               ntgzs = len(tgzs)
          for tgz in tgzs[:ntgzs]: 
               print 'unpacking', tgz
               untar_exit_code = os.system('tar -zxf {}'.format(tgz))
               untar_exit_code_sum += untar_exit_code
               # tgz is e.g. heppyOutput_43.tgz
               # so index is 43
               index = int(os.path.splitext(tgz)[0].split('_')[1]) + subdid
               if not untar_exit_code == 0:
                    os.system("echo 'Problem with sample {}, chunk {}, version {}, submitted on {}' >> $CMSSW_BASE/src/CMGTools/H2TauTau/scripts/tgzs_problems.log".format(
                              info['sample'],
                              index,
                              info['sample_version'],
                              info['sub_date']))
               else:
                    chunkname = '{}_Chunk{}'.format(info['name'], index)
                    chunks[subd].append(chunkname)
                    os.rename('Output', '../'+chunkname)
                    os.remove(tgz)
          os.chdir(destpath)
          shutil.rmtree(subd)
     os.chdir(oldpath)
     return untar_exit_code_sum
          
