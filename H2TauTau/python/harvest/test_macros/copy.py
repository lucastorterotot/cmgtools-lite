import os 
import shutil 

meta = {
    'foo' : 'bar'
}

def process(dataset_path): 
    fname = 'NtupleProducer/tree.root'
    srcfile = os.path.join(dataset_path,fname)
    tmpfile = 'tmp.root'
    shutil.copyfile(srcfile, tmpfile)
    return tmpfile, fname
