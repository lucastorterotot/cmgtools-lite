#!/usr/bin/env python

import os 
import subprocess
import re
import shutil
import fnmatch
from ROOT import TFile

from backends import lyonXRD

class Dataset(object):
    
    def __init__(self, path, subdirs='*', tgzs='*',
                 fhandler=lyonXRD):
        '''Create a dataset. 

        parameters: 

        path: LFN, e.g. 
            /store/user/gtouquet/heppyTrees/190503/tt_DY_nominal/DYJetsToLL_M50/190505_112304
        subdirs: wildcard pattern for the subdirs to consider
            a subdir is e.g. 0000
        fhandler: filesystem backend. for now, only xrootd is working, don't use GFAL

        attributes: 

        path: e.g. /store/user/gtouquet/heppyTrees/190503/tt_DY_nominal/DYJetsToLL_M50/190505_112304
        name: e.g. /DYJetsToLL_M50
        subdirs: list of subdirectories, e.g. 0000
        tgzs: dictionary of tar files per subdirectory
        chunks: dictionary of chunks per subdirectory
        '''
        self.path = path
        self.name = self.path.split('/')[-2]
        self.fhandler=fhandler
        self.subdir_pattern = subdirs
        self.tgz_pattern = tgzs
        self.subdirs = self.find_subdirs(path)
        self.tgzs = dict()
        for subd in self.subdirs:
            self.tgzs[subd] = self.find_tgzs(subd)
        # destination directory on local machine,
        # will be set at fetching
        self.dest = None
        # will be filled at unpacking:
        self.chunks = None

    def __str__(self): 
        lines = ['name: {}\npath: {}'.format(self.name,
                                             self.path)]
        lines.append('subdirs:')
        for subd in self.subdirs: 
            lines.append(subd)
            lines.extend(self.tgzs[subd])
            if self.chunks == None:
                lines.append('unpacking not done')
            else: 
                lines.append('chunks:')
                lines.extend(self.chunks[subd])
        return '\n'.join(lines)

    def abspath(self, path):
        '''return absolute path from a relative path within the dataset'''
        return '/'.join([self.path, path])

    def find_subdirs(self, path):
        '''Look for subdirs within the dataset. 
        Subdirs are subdirectories with a name composed of 4 digits, most often
        0000

        COLIN: shouldn't we remove the possibility to filter subdirs 
        according to subdir_pattern? 
        '''
        subdirs = self.fhandler.ls(self.path)
        pattern = re.compile('\d{4}$')
        subdirs = [os.path.basename(subd) for subd in subdirs if pattern.search(subd)
                   and fnmatch.fnmatch(subd, self.subdir_pattern)]
        return subdirs

    def find_tgzs(self, subd):
        '''Find compressed archives in a subdir'''
        subd = self.abspath(subd)
        files = self.fhandler.ls(subd)
        files = [os.path.basename(f) for f in files if f.endswith('.tgz')
                 and fnmatch.fnmatch(f, self.tgz_pattern)]
        return files

    def fetch(self, dest=None):
        '''fetch the dataset and put it into a destination path.
        
        if dest exists, its contents are deleted
        if dest does not exist, it is set e.g. to 
        tt_DY_nominal/DYJetsToLL_M50/0000/
        if the dataset path is 
        /store/user/gtouquet/heppyTrees/190503/tt_DY_nominal/DYJetsToLL_M50/190505_112304/0000
        I have no idea why (colin)
        '''
        if dest is None: 
            #COLIN : Why? What happens if we have more directories
            # like 180625_123805? 
            # it seems to me that this tries to solve a problem that 
            # should have been solved downstream
            dest = '/'.join(self.path.split('/')[-3:-1])
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
        '''Not used yet, need to find a way to check output
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
        '''unpacks the dataset after fetching. 
        fetches if fetching not yet done. 
        each tgz file is unpacked into an heppy chunk, 
        for later heppy_hadd
        '''
        if self.dest is None:
            print 'dataset was not fetched, fetching now'
            self.fetch()
        basepath=os.getcwd()
        os.chdir(self.dest)
        destpath = os.getcwd()
        self.chunks = dict()
        for subd, tgzs in self.tgzs.iteritems():
            print 'unpacking subdir', subd
            os.chdir(subd)
            self.chunks[subd] = []
            for tgz in tgzs: 
                print 'unpacking', tgz
                os.system('tar -zxf {}'.format(tgz))
                # tgz is e.g. heppyOutput_43.tgz
                # so index is 43
                index = os.path.splitext(tgz)[0].split('_')[1]
                chunkname = '{}_Chunk{}'.format(self.name, index)
                self.chunks[subd].append(chunkname)
                os.rename('Output', chunkname)
                os.remove(tgz)
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
    parser.add_option("-F", "--ff", dest="apply_ff",
                      action="store_true", default=False,
                      help='whether or not to add fake factors to trees')
    parser.add_option("-c", "--convert", dest="convert_ntuple",
                      action="store_true", default=False,
                      help='whether or not to use convert_ntuple.py to convert the output tree')
 
    
    (options,args) = parser.parse_args()
    if len(args)!=1:
        print parser.usage
        sys.exit(1)
    return options, args

def harvest(src, subdir_pattern='*', tgz_pattern='*', convert_ntuple=False):
    print(src, subdir_pattern, tgz_pattern)
    ds = Dataset(src, 
                 subdirs=subdir_pattern, 
                 tgzs=tgz_pattern)
    if ds.fetch():
        print(ds.dest)
        import pdb; pdb.set_trace()
        ds.unpack()
        ds.hadd()
        compname=ds.dest[ds.dest.find('/')+1:]
        if len(ds.subdirs) > 1:
            paths_to_hadd = [ds.dest+'/'+subdir+'/'+compname+'/NtupleProducer/tree.root' for subdir in ds.subdirs]
            command = 'hadd '+ds.dest+'/tree.root'
            command = ' '.join([command]+paths_to_hadd)
            os.system(command)
        else:
            os.system('mv '+ds.dest+'/'+ds.subdirs[0]+'/'+compname+'/NtupleProducer/tree.root '+ds.dest+'/tree.root')
        for subdir in ds.subdirs:
            os.system('rm -rf '+ds.dest+'/'+subdir+' &')
        if convert_ntuple:
            convert_ntuple_cmd = "if [[ $PYTHONPATH == *HTT/sync* ]] ; then "
            convert_ntuple_cmd+= 'convert_ntuple.py '+ds.dest+'/tree.root'+" 'b' -o "+ds.dest+'/tree_converted.root'
            convert_ntuple_cmd+= ' && mv '+ds.dest+'/tree_converted.root '+ds.dest+'/tree.root '
            convert_ntuple_cmd+= "; else echo 'Hey, please initialize HTT/sync! Ntuple not converted.' ; fi"
            os.system(convert_ntuple_cmd)


if __name__ == '__main__':

    options, args = get_options()
    src = args[0]
    harvest(src, 
            subdir_pattern=options.subdir_pattern, 
            tgz_pattern=options.tgz_pattern, 
            apply_ff=options.apply_ff, 
            convert_ntuple=options.convert_ntuple)
