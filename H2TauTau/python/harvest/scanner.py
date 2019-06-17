from backends import lyonXRD as fhandler
from dataset import Dataset
from datasetdb import DatasetDB
import fnmatch
import os
import re

class Scanner(object): 
    '''Dataset scanner'''

    def __init__(self, path, pattern='*', writedb_asap=False):
        '''create scanner
        
        path: base directory
        pattern: dataset pattern on full path
        '''
        self.path = path
        self.pattern = pattern
        self.writedb_asap = writedb_asap
        self.database = None
        self.datasets = self._start_scan()

    def writedb(self, datasets=None):
        '''write datasets to the db'''
        if not self.database :
            self.database = DatasetDB('writer')
        if datasets is None: 
            datasets = self.datasets
        for ds in datasets: 
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
                print(path)
                dataset = Dataset(path)
                results.append(dataset)
                if self.writedb_asap: 
                    self.writedb([dataset])
                break
            else: 
                results.extend( self._scan(subdir, level+1))
        return results
        
