from CMGTools.H2TauTau.harvest.subdirscanner import SubdirScanner 
import pprint

if __name__ == '__main__':
     basedir = '/gridgroup/cms/touquet/crab_submission_dirs'
     scanner = SubdirScanner(basedir, db='datasets')
     scanner.scan()
     scanner.writedb()
     print('{} datasets written to database'.format(len(scanner.infos)))

