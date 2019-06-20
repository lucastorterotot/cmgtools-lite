import os
import re
import subprocess
from scanner import Scanner 

class SubdirScanner(Scanner):
    '''Scan submission directory to find datasets'''

    def __init__(self, path):
        super(SubdirScanner, self).__init__(path)

    def _scan(self, path): 
        '''Scan path to find datasets. 

        returns the list of dataset info dicts
        '''
        self.dirs = self._find_dirs(path)
        self.infos = self._extract_info(self.dirs)
        return self.infos

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
