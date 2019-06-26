#!/usr/bin/env python

import os 
import subprocess
import re
import shutil
import fnmatch

class GFAL(object):
    '''GFAL backend. Should we remove it?'''

    def __init__(self, run=True):
        self.rprefix = 'srm://lyogrid06.in2p3.fr:8446/srm/managerv2?SFN=/dpm/in2p3.fr/home/cms/data'
        self.lprefix = 'file:'
        self.run = run

    def _file(self, path):
        if path.startswith('/store'):
            return ''.join([self.rprefix, path])
        else:
            return ''.join([self.lprefix, path])

    def _run(self, cmd):
        pipe = subprocess.Popen(cmd.split(),stdout=subprocess.PIPE)
        return pipe.communicate()[0]

    def ls(self, path, opt=None):
        if opt: 
            cmd = 'gfal-ls {opt} {path}'.format( opt=opt, 
                                                 path=self._file(path))
        else: 
            cmd = 'gfal-ls {path}'.format(path=self._file(path))    
        if self.run: 
            return self._run(cmd).splitlines() 
        else:
            return cmd

    def cp(self, src, dest, opt=None):
        if opt: 
            cmd = 'gfal-copy {opt} {src} {dest}'.format( 
                opt=opt, 
                src=self._file(src),
                dest=self._file(dest)
                )
        else: 
            cmd = 'gfal-copy {src} {dest}'.format(
                src=self._file(src),
                dest=self._file(dest)
                )    
        if self.run: 
            return self._run(cmd).splitlines() 
        else:
            return cmd

gfal = GFAL()

class XRD(object):
    '''xrootd backend, currently in use'''

    def __init__(self, run=True, host='lyogrid06.in2p3.fr', 
                 prefix='/dpm/in2p3.fr/home/cms/data'):
        '''Create xrootd backend'''
        self.host = host
        self.prefix = prefix
        self.lprefix = ''
        self.run = run

    def _file(self, path):
        '''returns file path, given an LFN or a local directory'''
        if path.startswith('/store'):
            return False, ''.join([self.prefix, path])
        else:
            return True, ''.join([self.lprefix, path])

    def _run(self, cmd):
        '''run a command'''
        pipe = subprocess.Popen(cmd.split(),stdout=subprocess.PIPE)
        return pipe.communicate()[0]

    def lfn(self, path): 
        '''returns logical file name (LFN)'''
        if path.startswith('/store'): 
            return path
        pos = path.find('/store')
        if pos < 0: 
            raise( ValueError('{} is not on the SE!'.format(path) ) )
        lfn = path[pos:] 
        return lfn

    def ls(self, path, opt=''):
        local, path = self._file(path)
        if not local: 
            cmd = 'xrdfs {host} ls {opt} {path}'.format(
                opt=opt, 
                host=self.host,
                path=path)
        else: 
            cmd = 'ls {path}'.format(path=path)
        if self.run: 
            paths = self._run(cmd).splitlines()
            # files = [os.path.basename(path) for path in paths]
            return paths
        else:
            return cmd

    def cp(self, src, dest):
        local, src = self._file(src)
        if not local: 
            src = 'root://{}/{}'.format(self.host, src)
        local, dest = self._file(dest)
        if not local: 
            dest = 'root://{}/{}'.format(self.host, dest)
        cmd = 'xrdcp {src} {dest}'.format( 
            src=src,
            dest=dest
            )
        if self.run: 
            return self._run(cmd).splitlines() 
        else:
            return cmd

lyonXRD = XRD()

