from backends import lyonXRD as fhandler
from dataset import Dataset
from scanner import Scanner
import fnmatch
import os
import re

class SEScanner(Scanner): 
    '''Scan the storage element to find datasets'''

    def __init__(self, path, pattern='*', writedb_asap=False):
        '''create scanner
        
        path: base directory
        pattern: dataset pattern on full path
        '''
        super(SEScanner, self).__init__(path, pattern, writedb_asap)


    def _scan(self, path, level=0):
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
                dataset = Dataset(path)
                info = dataset.info()
                results.append(info)
                if self.writedb_asap: 
                    self.writedb([info])
                break
            else: 
                results.extend( self._scan(subdir, level+1))
        return results
        
