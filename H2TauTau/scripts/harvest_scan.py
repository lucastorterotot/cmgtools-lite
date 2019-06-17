from CMGTools.H2TauTau.harvest.scanner import Scanner 

if __name__ == '__main__':
     path = '/store/user/gtouquet/heppyTrees/190503'
#      pattern = '*tt_DY_Btagging*'
     pattern = '*'
     scanner = Scanner(path, pattern, writedb_asap=True)
