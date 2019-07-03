'''
select di-taus with l1_pt > 100
'''

from ROOT import TFile 
import os 

cut = 'l1_pt>100'

meta = {
    'cut':cut
}

def process(dataset_path):  
    path_in_dataset = 'NtupleProducer/tree.root'
    ifile = TFile( os.path.join(dataset_path, path_in_dataset) )
    itree = ifile.Get('events')
    ofname = 'output.root'
    ofile = TFile(ofname, 'recreate')
    otree = itree.CopyTree(cut)
    ofile.Write()
    return ofname, path_in_dataset

if __name__ == '__main__':
    print(process('tree.root'))
