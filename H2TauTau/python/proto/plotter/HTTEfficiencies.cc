#include <vector>

#include "TFile.h"
#include "RooWorkspace.h"
#include "RooRealVar.h"
#include "RooFunctor.h"

double getTauIDWeight(double pt, double eta, double dm, int channel) { // yeah double dm
    // auto ws = EffProvider::instance().ws();
    // RooFunctor* tau_id_weight = ws.function("t_iso_mva_t_pt40_eta2p1_sf")->functor(ws.argSet("t_pt,t_eta,t_dm"));
    // auto args = std::vector<double>{pt, eta, dm};
    // auto weight = tau_id_weight->eval(args.data());
    // std::cout << "Tau ID weight for pt, eta, dm" << pt << ", " << eta << ", " << dm << " is " << weight << std::endl;
  if (channel == 0)//FF
    return 0.99;
  if (channel == 1)//tt
    return 0.97;
  if (channel == 2)//mt
    return 0.95;
}

double getMuToTauWeightLoose(double eta) {
    auto aeta = std::abs(eta);
    if (aeta < 0.4)
        return 1.22;
    if (aeta < 0.8)
        return 1.12;
    if (aeta < 1.2)
        return 1.26;
    if (aeta < 1.7)
        return 1.22;
    if (aeta < 2.3)
        return 2.39;
    return 1.;
}

double getEToTauWeightVLoose(double eta) {
    auto aeta = std::abs(eta);
    if (aeta < 1.5)
        return 1.21;
    if (aeta > 1.5)
        return 1.38;
    return 1.;
}

double getTauWeight(int gen_match, double pt, double eta, double dm, int channel) {
    if (gen_match == 5)
      return getTauIDWeight(pt, eta, dm, channel);
    if (gen_match == 2 || gen_match == 4)
        return getMuToTauWeightLoose(eta);
    if (gen_match == 1 || gen_match == 3)
        return getEToTauWeightVLoose(eta);
    return 1.;
}
