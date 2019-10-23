#!/usr/bin/env python

import os 
import subprocess
import re
import shutil
import fnmatch
import pprint

from backends import lyonXRD

class Dataset(object):
    
    info_pattern = re.compile(r'.*(\d{6})/(.*)/(.*)/(.*)$')

    def __init__(self, path_or_info, subdirs='*', tgzs='*',
                 fhandler=lyonXRD):
        '''Create a dataset. 

        parameters: 

        path_or_info: LFN, e.g. 
            /store/user/gtouquet/heppyTrees/190503/tt_DY_nominal/DYJetsToLL_M50/190505_112304
            or an info dictionary extracted from the database. 

        The following arguments are only important if path_or_info is an LFN. 

        subdirs: wildcard pattern for the subdirs to consider
            a subdir is e.g. 0000
        fhandler: filesystem backend. for now, only xrootd is working, don't use GFAL
        '''
        self.fhandler = fhandler
        if isinstance(path_or_info, basestring):
            self.path = path_or_info
            self._info = self._extract_info(path_or_info, tgzs, subdirs)
        else: 
            self.path = path_or_info['path']
            self._info = path_or_info

    def _extract_info(self, path, tgz_pattern, subdir_pattern): 
        '''extract information from path on storage element'''
        name = path.split('/')[-2]
        subdirs = self.find_subdirs(path, subdir_pattern)
        tgzs = dict()
        for subd in subdirs:
            tgzs[subd] = self.find_tgzs(subd, tgz_pattern)
        m = self.__class__.info_pattern.match(path)
        prod_date, sample_version, sample, write_date = m.groups()    
        info = dict(
            name = '{}%{}%{}'.format(
                prod_date, sample, sample_version
                ),
            sample = sample,
            prod_date = prod_date,
            write_date = write_date,
            sample_version = sample_version,
            path = path,
            subdir_pattern = subdir_pattern,
            tgz_pattern = tgz_pattern,
            subdirs = subdirs,
            tgzs = tgzs
            )        
        return info

    def info(self):
        '''return dataset information as a dictionary, 
        for storage into the db
        '''
        return self._info

    def __str__(self): 
        return pprint.pformat(self._info)

    def __repr__(self): 
        return 'dataset: {}'.format(self._info['name'])

    def abspath(self, path):
        '''return absolute path from a relative path within the dataset'''
        return '/'.join([self.path, path])

    def find_subdirs(self, path, subdir_pattern):
        '''Look for subdirs within the dataset. 
        Subdirs are subdirectories with a name composed of 4 digits, most often
        0000

        COLIN: shouldn't we remove the possibility to filter subdirs 
        according to subdir_pattern? 
        '''
        subdirs = self.fhandler.ls(path)
        pattern = re.compile('\d{4}$')
        subdirs = [os.path.basename(subd) for subd in subdirs 
                   if pattern.search(subd)
                   and fnmatch.fnmatch(subd, subdir_pattern)]
        return subdirs

    def find_tgzs(self, subd, tgz_pattern):
        '''Find compressed archives in a subdir'''
        subd = self.abspath(subd)
        files = self.fhandler.ls(subd)
        files = [os.path.basename(f) for f in files if f.endswith('.tgz')
                 and fnmatch.fnmatch(f, tgz_pattern)]
        return files



if __name__ == '__main__':

    options, args = get_options()
    src = args[0]
    harvest(src, 
            subdir_pattern=options.subdir_pattern, 
            tgz_pattern=options.tgz_pattern, 
            apply_ff=options.apply_ff, 
            convert_ntuple=options.convert_ntuple
            )
