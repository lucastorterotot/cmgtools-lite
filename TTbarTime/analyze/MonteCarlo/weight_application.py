from MC_definitions import *
from ROOT import TCanvas, TFile, TH1F, TTree, TLegend, THStack
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("variable", help="choose variable of TTree")
args = parser.parse_args()


