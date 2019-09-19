from CMGTools.H2TauTau.harvest.subdirscanner import SubdirScanner 
from CMGTools.H2TauTau.harvest.datasetdb import DatasetDB

from getpass import getpass

if __name__ == '__main__':
     basedir = '/gridgroup/cms/touquet/crab_submission_dirs'
     pwd = getpass()
     dsdb = DatasetDB('writer', pwd, db='datasets')
     scanner = SubdirScanner(basedir, dsdb)
     scanner.scan()
     scanner.writedb()
     print('{} datasets written to database'.format(len(scanner.infos)))

