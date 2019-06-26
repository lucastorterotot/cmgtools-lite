import os
import sys 
from dataset import Dataset

def get_options():
    '''process command line options and return options, args'''
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
