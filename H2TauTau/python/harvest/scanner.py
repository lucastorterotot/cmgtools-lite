from backends import lyonXRD as fhandler
from dataset import Dataset
from datasetdb import DatasetDB
import fnmatch
import os
import re

class Scanner(object): 
    '''Dataset scanner'''

    def __init__(self, path ,pattern='*'):
        '''create scanner
        
        path: base directory
        pattern: dataset pattern on full path
        '''
        self.path = path
        self.pattern = pattern
        self.datasets = self._start_scan()
        self.database = None

    def writedb(self):
        '''write datasets to the db'''
        if not self.database :
            self.database = DatasetDB('writer')
        for ds in self.datasets: 
            self.database.insert(ds.info())
            

    def _start_scan(self):
        '''initiate recursive scan'''
        print('scanning {} ({}) please be patient...'.format(self.path, 
                                                             self.pattern))
        return self._scan(self.path)

    def _scan(self, path, level=0):
        '''recursive scan to find datasets.

        directories containing a subirectory with 4 digits, eg. 0000,
        are considered a dataset
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
                # print('found', path, basename)
                results.append(Dataset(path))
                break
            else: 
                results.extend( self._scan(subdir, level+1))
        return results
        
