import os
import re
import subprocess
import pprint
import copy
from collections import Counter
from scanner import Scanner 

class SubdirScanner(Scanner):
    '''Scan submission directory to find datasets'''

    def __init__(self, *args, **kwargs):
        super(SubdirScanner, self).__init__(*args, **kwargs)

    def _scan(self, path): 
        '''Scan path to find datasets. 

        returns the list of dataset info dicts
        '''
        self.dirs = self._find_dirs(path)
        infos = self._extract_info(self.dirs)
        self.infos = self._remove_duplicates(infos)
        return self.infos


    def _remove_duplicates(self, infos):
        '''removes duplicate infos. 

        if several infos have the same name, the one with the latest sub_date is kept.
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
                latest = max(infos_with_this_name, key=lambda x: x['sub_date'])
                no_dupes.append(latest)
            # remove this name from the dictionary, 
            # so that the latest info is not added several times
            del by_name[info['name']]
        return no_dupes


    def _extract_info(self, dirs):
        '''extract dataset information for a list of directories

        returns the list of dataset info dicts
        '''
        pattern = re.compile(r'.*crab_.*/crab_(.*)_(\d+)_(.*)_(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})$')
        infos = []
        filtered_dirs = []
        for path in dirs: 
            m = pattern.match(path)
            if m: 
                sample, prod_date, sample_version, sub_date = m.groups()
                info = dict(
                    name = '{}%{}%{}'.format(
                        prod_date, sample, sample_version
                        ),
                    sub_dir = path,
                    sample = sample,
                    prod_date = prod_date, 
                    sample_version = sample_version, 
                    sub_date = sub_date
                    )
                infos.append(info)
                filtered_dirs.append(path)
        self.dirs = filtered_dirs
        return infos


    def _find_dirs(self, path, pattern=None):
        if pattern: 
            cmd = 'find {} -type d -iname {}'.format(path, pattern)
        else: 
            cmd = 'find {} -type d'.format(path)        
        result = subprocess.check_output(cmd.split())
        dirs = result.splitlines()
        dirs = [path for path in dirs if 
                not path.endswith('results') and 
                not path.endswith('inputs')]
        return dirs
