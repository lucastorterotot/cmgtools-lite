#!/usr/bin/env python

import os 
import subprocess
import re
import shutil
import fnmatch
from ROOT import TFile

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

    def __init__(self, run=True, host='lyogrid06.in2p3.fr', prefix='/dpm/in2p3.fr/home/cms/data'):
        self.host = host
        self.prefix = prefix
        self.lprefix = ''
        self.run = run

    def _file(self, path):
        if path.startswith('/store'):
            return 'root://{}/{}/{}'.format(self.host,self.prefix, path)
        else:
            return ''.join([self.lprefix, path])

    def _run(self, cmd):
        pipe = subprocess.Popen(cmd.split(),stdout=subprocess.PIPE)
        return pipe.communicate()[0]

    def ls(self, path, opt=''):
        cmd = 'xrdfs {host} ls {opt} {prefix}/{path}'.format(
            opt=opt, 
            host=self.host,
            prefix=self.prefix,
            path=path)
        if self.run: 
            paths = self._run(cmd).splitlines()
            files = [os.path.basename(path) for path in paths]
            return files
        else:
            return cmd

    def cp(self, src, dest, opt=''):
        cmd = 'xrdcp {opt} {src} {dest}'.format( 
            opt=opt, 
            src=self._file(src),
            dest=self._file(dest)
            )
        if self.run: 
            return self._run(cmd).splitlines() 
        else:
            return cmd

lyonXRD = XRD()

