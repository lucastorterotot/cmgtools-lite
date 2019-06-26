
from CMGTools.H2TauTau.harvest.datasetdb import DatasetDB

def option_parser():
     from optparse import OptionParser
     usage = "usage: %prog [options]"
     parser = OptionParser(usage=usage)
     parser.add_option("-d", "--dataset-pattern", dest="dataset_pattern",
                       default='*',
                       help='dataset pattern')
     parser.add_option("-n", "--negate", dest="negate",
                       action="store_true", default=False,
                       help='do nothing')
    (options,args) = parser.parse_args()
    if len(args)!=0:
        print parser.usage
        sys.exit(1)
    return options, args


if __name__ == '__main__':
     basedir = '/gridgroup/cms/touquet/crab_submission_dirs'
     db = 'datasets'
     scanner = SubdirScanner(basedir, db=db)
     scanner.scan()
     scanner.writedb()
     print('{} datasets written to database'.format(len(scanner.datasets)))

