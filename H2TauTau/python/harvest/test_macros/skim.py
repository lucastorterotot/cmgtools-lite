'''
select di-taus with l1_pt > 100
'''

from ROOT import TFile 
import os 

cut = "Flag_goodVertices && Flag_globalTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_BadChargedCandidateFilter && Flag_ecalBadCalibFilter && (!veto_extra_elec) && (!veto_extra_muon) && l2_againstElectronVLooseMVA6 && l2_againstMuonLoose3 && l2_byVLooseIsolationMVArun2017v2DBoldDMwLT2017 && l1_byVLooseIsolationMVArun2017v2DBoldDMwLT2017 && l1_againstElectronVLooseMVA6 && l1_againstMuonLoose3"

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
