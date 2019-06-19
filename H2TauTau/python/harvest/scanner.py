from backends import lyonXRD as fhandler
from dataset import Dataset
from datasetdb import DatasetDB
import fnmatch
import os
import re

class Scanner(object): 
    '''Base scanner'''

    def __init__(self, path, pattern='*', writedb_asap=False):
        '''create scanner
        
        path: base directory
        pattern: dataset pattern on full path
        '''
        self.path = path
        self.pattern = pattern
        self.writedb_asap = writedb_asap
        self.database = None
        self.datasets = None

    def writedb(self, datasets=None):
        '''write datasets to the db'''
        if not self.database :
            self.database = DatasetDB('writer')
        if datasets is None: 
            datasets = self.datasets
        for ds in datasets: 
            self.database.insert(ds.info())
            
        
