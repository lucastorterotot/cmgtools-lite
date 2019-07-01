from CMGTools.H2TauTau.harvest.se_scanner import SEScanner  as Scanner

if __name__ == '__main__':
     path = '/store/user/gtouquet/heppyTrees/190503'
     pattern = '*tt_DY_Btagging*'
     # pattern = '*'
     scanner = Scanner(path, pattern, db='datasets')
     scanner.scan()
     scanner.writedb()
     print('{} datasets written to database'.format(len(scanner.infos)))
