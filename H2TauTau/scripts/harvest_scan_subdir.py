from CMGTools.H2TauTau.harvest.subdirscanner import SubdirScanner 
import pprint

if __name__ == '__main__':
     basedir = '/gridgroup/cms/touquet/crab_submission_dirs'
     db = 'datasets'
     scanner = SubdirScanner(basedir, db=db)
     scanner.scan()
     scanner.writedb()
     print('{} datasets written to database'.format(len(scanner.datasets)))

