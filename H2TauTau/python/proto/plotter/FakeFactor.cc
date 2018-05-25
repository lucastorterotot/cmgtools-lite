
#include <TROOT.h>
#include <TFile.h>
#include <TTree.h>
#include <TH2D.h>
#include <iostream>
#include "HTTutilities/Jet2TauFakes/interface/FakeFactor.h"

class FFProvider {
public:
    static FFProvider& instance() {
        static FFProvider instance;
        return instance;
    }

    FakeFactor& FF() const {
        return *ff;
    }

private:
    FFProvider() {
        f_in = new TFile("$CMSSW_BASE/src/HTTutilities/Jet2TauFakes/data/tt/inclusive/fakeFactors_20170628_medium.root");
        std::cout << "Creating FFProvider instance" << std::endl;
	ff = (FakeFactor*)f_in->Get("ff_comb");
    }

    ~FFProvider() {
	delete ff;
	delete f_in;
    }

    TFile* f_in;
    FakeFactor* ff;
};


double getFFWeight(double tau_pt, double tau2_pt, int decay_mode, int njets, double mvis, double mt_tot) {
    FakeFactor& ff = FFProvider::instance().FF();
    std::vector<double> inputs(6);
    inputs[0] = tau_pt;
    inputs[1] = tau2_pt; //pt of non-fake tau candidate
    inputs[2] = decay_mode;
    inputs[3] = njets;
    inputs[4] = mvis;
    inputs[5] = mt_tot;
    double weight = ff.value(inputs);
    return weight;
}
