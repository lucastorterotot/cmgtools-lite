'''
select di-taus with l1_pt > 100
'''

from ROOT import TFile 
import os 
import shutil
import tempfile

cut = "Flag_goodVertices && Flag_globalTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_BadChargedCandidateFilter && Flag_ecalBadCalibFilter && (!veto_extra_elec) && (!veto_extra_muon) && l2_againstElectronVLooseMVA6 && l2_againstMuonLoose3 && l2_byVLooseIsolationMVArun2017v2DBoldDMwLT2017 && l1_byVLooseIsolationMVArun2017v2DBoldDMwLT2017 && l1_againstElectronVLooseMVA6 && l1_againstMuonLoose3"

meta = {
    'cut':cut
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
    otree = itree.CopyTree(cut)
    print('skimmed from {} to {} entries'.format(
            itree.GetEntries(),
            otree.GetEntries()
            )
          )
    ofile.Write()
    os.remove(tmpfname)
    return ofname, path_in_dataset

if __name__ == '__main__':
    print(process('tree.root'))
