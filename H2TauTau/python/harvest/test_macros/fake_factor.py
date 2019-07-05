'''
Apply fake factors
'''

from ROOT import TFile 
import os 
import shutil
import tempfile
import HTTutilities.Jet2TauFakes.FakesAdd as FakesAdd

channel = 'tt'

meta = {
    'channel' : channel,
    'FF_file' : os.path.expandvars(FakesAdd.FF_file.format(channel)),
    'frac_file' : FakesAdd.frac_file
}

def process(dataset_path):  
    path_in_dataset = 'NtupleProducer/tree.root'
    ifname =  os.path.join(dataset_path, path_in_dataset)
    tmpfname = tempfile.mktemp('.root',prefix='/scratch/tmp')
    shutil.copyfile(ifname, tmpfname)
    ifile = TFile(tmpfname)
    itree = ifile.Get('events')
    ofname = tempfile.mktemp('.root',prefix='/scratch/tmp')
    ofile = TFile(ofname, 'recreate')
    systematics = False
    if 'nominal' in dataset_path:
        systematics = True
    FakesAdd.FakesAdd(ifile, ofile, systematics = systematics, channel = channel)
    ofile.Write()
    os.remove(tmpfname)
    return ofname, path_in_dataset

if __name__ == '__main__':
    print(process('tree.root'))
