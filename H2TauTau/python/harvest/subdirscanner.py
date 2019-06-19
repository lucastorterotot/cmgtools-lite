import os
import re
import subprocess

class SubdirScanner(object):
    '''Scan submission directories to find datasets'''

    def scan(self, basedir): 
        self.dirs = self._find_dirs(basedir)
        self.infos = self._extract_info(self.dirs)

    def _extract_info(self, dirs):
        pattern = re.compile(r'.*crab_.*/crab_(.*)_(\d+)_(.*)_(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})$')
        infos = []
        filtered_dirs = []
        for path in dirs: 
            m = pattern.match(path)
            if m: 
                base_sample, prod_date, sample, sub_date = m.groups()
                info = dict(
                    sub_dir = path,
                    base_sample = base_sample,
                    prod_date = prod_date, 
                    prod_name = sample, 
                    sub_date = sub_date
                    )
                infos.append(info)
                filtered_dirs.append(path)
        self.dirs = filtered_dirs
        return infos


    def _find_dirs(self, basedir, pattern=None):
        if pattern: 
            cmd = 'find {} -type d -iname {}'.format(basedir, pattern)
        else: 
            cmd = 'find {} -type d'.format(basedir)        
        result = subprocess.check_output(cmd.split())
        dirs = result.splitlines()
        dirs = [path for path in dirs if 
                not path.endswith('results') and 
                not path.endswith('inputs')]
        return dirs
