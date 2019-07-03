from CMGTools.H2TauTau.harvest.se_scanner import SEScanner  as Scanner
from CMGTools.H2TauTau.harvest.datasetdb import DatasetDB

from getpass import getpass

if __name__ == '__main__':
     path = '/store/user/gtouquet/heppyTrees/190503'
     # pattern = '*tt_DY_Btagging*'
     pattern = '*'
     pwd = getpass()
     dsdb = DatasetDB('writer', pwd, db='datasets')
     scanner = Scanner(path, dsdb, pattern)
     scanner.scan()
     scanner.writedb()
     print('{} datasets written to database'.format(len(scanner.infos)))
