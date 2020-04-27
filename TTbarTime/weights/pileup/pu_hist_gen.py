import sys,os
from optparse import OptionParser
from ROOT import TFile, TH1D, TTree

from   PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption

usage = "usage: python pu_hist_gen.py [options] \n example: python pu_hist_gen.py -l CRABtest -y year"
parser = OptionParser(usage=usage)
parser.add_option("-y","--year", dest='year', default="2016", help="year on which u want to run the PU")
parser.add_option("-l", "--prod_label", dest = "prod_label",
                      default='MC_PU',
                      help='The prod label or part of prod labels to be selected.')
parser.add_option("-g", "--get_files", dest="get_files",
                      action="store_true", default=False,
                      help='whether or not to get the PU files')
options,args = parser.parse_args()

print options

if options.year == '2016':
    from CMGTools.TTbarTime.proto.samples.summer16.ttbar2016 import mc_ttbar
else: 
    from CMGTools.TTbarTime.proto.samples.fall17.ttbar2017 import mc_ttbar


samples=[]
dir_input  = "./files/"+options.year+"/"
if options.get_files:
    if not os.path.exists(dir_input):
        '''
        create the input file path
         '''
        print "here am I creating input directory" 
        os.makedirs(dir_input)
    samples=os.listdir("../../scripts/"+options.prod_label)
    os.chdir(dir_input)
    for i in samples:
        os.system("cp -r ../../../../scripts/"+options.prod_label+"/"+i+" . ") 
    os.chdir("../../")

dir_output = "./"+options.year+"/"
if not os.path.exists(dir_output):
    os.mkdir(dir_output)

name_list = []
for i in mc_ttbar:
    #print '#'.join(i.dataset.split("/"))
    name_list.append('#'.join(i.dataset.split("/")))

file_names = os.listdir(dir_input)
file_names.sort()
#print file_names

rootfile = TFile(dir_output+"pileup.root", "RECREATE")
pu_file = []
pu_tree = []
pu_hist = []

for i in range(len(file_names)):
    pu_file.append(TFile(dir_input+file_names[i]+"/tree.root"))
    pu_tree.append(pu_file[i].Get('events'))
    #print "got tree of the sample:", file_names[i] 


#print len(file_names)
#for i in range(len(file_names)):
#    print file_names[i],name_list[i]
#exit()
 

rootfile = TFile(dir_output+"pileup.root", "RECREATE")
for i in range(len(file_names)):
    #print "projecting pu distribution of the sample:",i, file_names[i] 
    pu_hist.append(TH1D(name_list[i],"",200,0.,200.))
    pu_tree[i].Project(name_list[i], "pu")
    pu_hist[i].Write()

os.system("cp "+dir_output+"pileup.root ../../data/"+options.year+"/") 



