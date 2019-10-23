from CMGTools.H2TauTau.harvest.subdirscanner import SubdirScanner 
from CMGTools.H2TauTau.harvest.datasetdb import DatasetDB

from getpass import getpass

import os

if __name__ == '__main__':
     basedir = '/gridgroup/cms/{}/crab_submission_dirs'.format(os.environ['USER'])
     pwd = getpass()
     dsdb = DatasetDB('writer', pwd, db='datasets')
     scanner = SubdirScanner(basedir, dsdb)
     scanner.scan()
     scanner.writedb()
     print('{} datasets written to database'.format(len(scanner.infos)))

