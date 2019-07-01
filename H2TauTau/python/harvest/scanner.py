from backends import lyonXRD as fhandler
from dataset import Dataset
from datasetdb import DatasetDB
import fnmatch
import os
import re

class Scanner(object): 
    '''Base scanner

    handles connection to database and defines user interface. 
    Child classes must implement: 

    _scan : scan the directory and return the dataset infos, 
            as a list of dictionaries 

    Important attributes: 
    - infos : list of info dicts for all infos. 
    '''

    def __init__(self, path, database, pattern='*'):
        '''create scanner
        
        path: base directory
        pattern: dataset pattern on full path
        '''
        self.path = path
        self.pattern = pattern
        self.database = database
        self.infos = None

    def writedb(self, infos=None):
        '''write infos to the db'''
        if infos is None: 
            infos = self.infos
        for ds in infos: 
            self.database.insert('se',ds)

    def scan(self):
        '''initiate recursive scan'''
        print('scanning {} ({}) please be patient...'.format(self.path, 
                                                             self.pattern))
        self.infos = self._scan(self.path)
        return self.infos

    def _remove_duplicates(self, infos, date_field):
        '''removes duplicate infos. 

        if several infos have the same name, the one with the latest date is kept.
        the ordering of the input list is preserved.
        '''
        by_name = dict()
        for info in infos:
            by_name.setdefault(info['name'], []).append(info)
        no_dupes = []
        for info in infos: 
            infos_with_this_name = by_name.get(info['name'], None)
            if infos_with_this_name is None: 
                # happens if latest info already added to no_dupes, 
                # see below
                continue
            ninfos = len(infos_with_this_name)
            if ninfos==1: 
                no_dupes.append(infos_with_this_name[0])
            else: 
                # using lexicographical comparison on sub_date. 
                # this assumes that sub_date is of the form: 
                # year month day hour min sec
                latest = max(infos_with_this_name, key=lambda x: x[date_field])
                no_dupes.append(latest)
            # remove this name from the dictionary, 
            # so that the latest info is not added several times
            del by_name[info['name']]
        return no_dupes
