#!/usr/bin/env python

import os 
import subprocess
import re
import shutil
import fnmatch
from ROOT import TFile

class GFAL(object):

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

class Dataset(object):
    
    def __init__(self,path,subdirs='*',tgzs='*',fhandler=lyonXRD):
        self.path = path
        self.name = self.path.split('/')[-2]
        self.fhandler=fhandler
        self.subdir_pattern = subdirs
        self.tgz_pattern = tgzs
        self.subdirs = self.find_subdirs(path)
        self.tgzs = dict()
        for subd in self.subdirs:
            self.tgzs[subd] = self.find_tgzs(subd)
        self.dest = None

    def abspath(self, path):
        return '/'.join([self.path, path])

    def find_subdirs(self,path):
        subdirs = self.fhandler.ls(self.path)
        pattern = re.compile('\d{4}$')
        subdirs = [subd for subd in subdirs if pattern.search(subd)
                   and fnmatch.fnmatch(subd, self.subdir_pattern)]
        return subdirs

    def find_tgzs(self, subd):
        subd = self.abspath(subd)
        files = self.fhandler.ls(subd)
        files = [f for f in files if f.endswith('.tgz')
                 and fnmatch.fnmatch(f, self.tgz_pattern)]
        return files

    def fetch(self, dest=None):
        if dest is None: 
            dest = '/'.join(self.path.split('/')[-2:])
        if os.path.isdir(dest):
            answer = None
            while answer not in ['y','n']:
                answer = raw_input('destination {} exists. continue? [y/n]'.format(dest))
            if answer == 'n':
                return False
            shutil.rmtree(dest)
        basepath=os.getcwd()
        os.makedirs(dest)
        self.dest = dest
        os.chdir(dest)
        destpath=os.getcwd()
        for subd, files in self.tgzs.iteritems():
            print 'fetching subdir', subd
            os.mkdir(subd)
            os.chdir(subd)
            for f in files:
                path = self.abspath('/'.join([subd, f]))
                print path
                # print self.fhandler.ls(path)
                self.fhandler.cp(path, '.')
            os.chdir(destpath)
        os.chdir(basepath)
        return True

    def check(self, pattern='*'):
        '''Not used do far, need to find a way to check output
        '''
        for subdir in self.tgzs:
            path = '{dest}/{subd}/'.format(dest=self.dest,
                                           subd=subdir)
            os.system('heppy_check.py {path}{pattern}'.format(path=path,
                                                              pattern=pattern))

    def hadd(self, path=''):
        for subdir in self.tgzs:
            if not path:
                path = '{dest}/{subd}/'.format(dest=self.dest,
                                               subd=subdir)
            os.system('heppy_hadd.py {path}'.format(path=path))
            os.system('rm -rf {path}/*Chunk*'.format(path=path))

    def unpack(self):
        if self.dest is None:
            print 'dataset was not fetched, fetching now'
            self.fetch()
        basepath=os.getcwd()
        os.chdir(self.dest)
        destpath = os.getcwd()
        for subd, files in self.tgzs.iteritems():
            print 'upackging subdir', subd
            os.chdir(subd)
            for i, f in enumerate(files): 
                print 'unpacking', f
                os.system('tar -zxf ' + f)
                os.rename('Output', 
                          '{}_Chunk{}'.format(self.name, str(i)))
                os.remove(f)
            os.chdir(destpath)
        os.chdir(basepath)

def get_options():
    import os
    import sys
    from optparse import OptionParser
    usage = "usage: %prog [options] <src_dir>"
    parser = OptionParser(usage=usage)
    parser.add_option("-t", "--tgz-pattern", dest="tgz_pattern",
                      default='*',
                      help='tgz pattern')
    parser.add_option("-s", "--subdir-pattern", dest="subdir_pattern",
                      default='*',
                      help='subdir pattern')
    parser.add_option("-S", "--skim", dest="skim", action='store_true',
                      default=False,
                      help='whether or not to skim ntuples KIT style')
 
    
    (options,args) = parser.parse_args()
    if len(args)!=1:
        print parser.usage
        sys.exit(1)
    return options, args


def skimntuple(ogpath, newpath):
    f = TFile(ogpath)

    tree = f.Get('events')
    newfile = TFile(newpath,'recreate')

    newtree = tree.CloneTree(0)

    for event in tree:
        if event.Flag_goodVertices and event.Flag_globalTightHalo2016Filter and event.Flag_HBHENoiseFilter and event.Flag_HBHENoiseIsoFilter and event.Flag_EcalDeadCellTriggerPrimitiveFilter and event.Flag_BadPFMuonFilter and event.Flag_BadChargedCandidateFilter and event.Flag_ecalBadCalibFilter and (not event.veto_extra_elec) and (not event.veto_extra_muon) and event.l2_againstElectronVLooseMVA6 and event.l2_againstMuonLoose3 and event.l2_byVLooseIsolationMVArun2017v2DBoldDMwLT2017 and event.l1_byVLooseIsolationMVArun2017v2DBoldDMwLT2017:
            newtree.Fill()

    newtree.Write()

def harvest(src, subdir_pattern='*', tgz_pattern='*', skim=False):
    print src, subdir_pattern, tgz_pattern
    ds = Dataset(src, 
                 subdirs=subdir_pattern, 
                 tgzs=tgz_pattern)
    if ds.fetch():
        print ds.dest
        ds.unpack()
        ds.hadd()
        if skim:
            ogpath = '{}/0000/{}/NtupleProducer/tree.root'.format(ds.dest,ds.dest[:ds.dest.find('/')])
            newpath = '{}/tree.root'.format(ds.dest[:ds.dest.find('/')])
            skimntuple(ogpath,newpath)
            os.system('rm -rf {}'.format(ds.dest))


if __name__ == '__main__':

    options, args = get_options()
    src = args[0]
    print src, options.subdir_pattern, options.tgz_pattern
    ds = Dataset(src, 
                 subdirs=options.subdir_pattern, 
                 tgzs=options.tgz_pattern)
    if ds.fetch():
        ds.unpack()
        ds.hadd()
        if options.skim:
            ogpath = '{}/0000/{}/NtupleProducer/tree.root'.format(ds.dest,ds.dest[:ds.dest.find('/')])
            newpath = '{}/tree.root'.format(ds.dest[:ds.dest.find('/')])
            skimntuple(ogpath,newpath)
            os.system('rm -rf {}'.format(ds.dest))
