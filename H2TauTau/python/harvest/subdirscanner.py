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
        self.infos = self._remove_duplicates(infos, 'sub_date')
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
                njobs = self._find_njobs(path)
                info = dict(
                    name = '{}%{}%{}'.format(
                        prod_date, sample, sample_version
                        ),
                    sub_dir = path,
                    sample = sample,
                    prod_date = prod_date, 
                    sample_version = sample_version, 
                    sub_date = sub_date, 
                    njobs = njobs
                    )
                infos.append(info)
                filtered_dirs.append(path)
        self.dirs = filtered_dirs
        return infos

    def _find_njobs(self, path): 
        '''Get number of jobs from the crab log. 
        taken from this line: 
        config.JobType.scriptArgs = ['dataset=W1JetsToLNu_LO', 'total=54', \
                'useAAA=full', 'cfgfile=diTau_2018_modular_cfg.py', 'cfgname=Btagging_up']
        '''
        pattern = re.compile('total=(\d+)')
        logfile = os.path.join(path,'crab.log')
        with open(logfile) as ifile: 
            for line in ifile: 
                if line.startswith('config.JobType.scriptArgs'):
                    m = pattern.search(line)
                    if m: 
                        return int(m.group(1))
                    else: 
                        assert(False)
        
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
