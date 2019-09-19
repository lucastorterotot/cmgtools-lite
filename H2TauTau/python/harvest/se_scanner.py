from backends import lyonXRD as fhandler
from dataset import Dataset
from scanner import Scanner
import fnmatch
import os
import re
import pprint

from multiprocessing import Pool

def _extract_info(path): 
    return Dataset(path).info() 

def _extract_info_multi(dirs): 
    p = Pool()  
    futures = []
    for path in dirs: 
        futures.append( p.apply_async(_extract_info, (path,)) )
    infos = []
    for future in futures: 
        infos.append(future.get())
    p.close()
    p.join()
    return infos

class SEScanner(Scanner): 
    '''Scan the storage element to find datasets'''

    def __init__(self, *args, **kwargs):
        '''create scanner
        
        path: base directory
        pattern: dataset pattern on full path
        '''
        super(SEScanner, self).__init__(*args, **kwargs)

    def _scan(self, path):
        dirs = self._find_dirs(path, level=0)
        infos = _extract_info_multi(dirs)
        infos = self._remove_duplicates(infos, 'write_date')
        return infos

    def _find_dirs(self, path, level=0):
        '''recursive scan to find datasets.

        directories containing a subirectory with 4 digits, eg. 0000,
        are considered a dataset

        returns the list of dataset info dicts
        '''
        # print('entering', path)
        if level>0 and not fnmatch.fnmatch(path, self.pattern):
            return []
        path = fhandler.lfn(path)
        # print('scan', path)
        results = []
        pattern = re.compile('\d{4}$')
        subdirs = fhandler.ls(path)
        for subdir in subdirs:
            basename = os.path.basename(subdir)
            if pattern.match(basename):
                print(path)
                # dataset = Dataset(path)
                # info = dataset.info()
                results.append(path)
                # if self.writedb_asap: 
                #    self.writedb([info])
                break
            else: 
                results.extend( self._find_dirs(subdir, level+1))
        return results
        
