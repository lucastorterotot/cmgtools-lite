from harvest import harvest
import os
from functools import partial
import multiprocessing as mp

def get_options():
    import os
    import sys
    from optparse import OptionParser
    usage = "usage: python multiHarvest.py [options] \n example: python multiHarvest.py -l CRABtest -d R -u gtouquet -C HiggsVBF125"
    parser = OptionParser(usage=usage)
    parser.add_option("-t", "--tgz-pattern", dest="tgz_pattern",
                      default='*',
                      help='tgz pattern')
    parser.add_option("-s", "--subdir-pattern", dest="subdir_pattern",
                      default='*',
                      help='subdir pattern')
    parser.add_option("-u", "--user", dest = "username",
                      default=os.environ['USER'],
                      help='the username to be used to look for files.')
    parser.add_option("-V", "--CMSSW_VERSION", dest = "cmssw_version",
                      default=os.environ['CMSSW_VERSION'],
                      help='Version of CMSSW used to produce the samples.')
    parser.add_option("-l", "--prod_label", dest = "prod_label",
                      default='diTau_2018_modular_cfg',
                      help='The prod label or part of prod labels to be selected.')
    parser.add_option("-C", "--component", dest = "cut_on_sample_names",
                      default="''",
                      help='Harvest only samples containing this string.')
    parser.add_option("-d", "--date", dest = "select_date",
                      default=None,
                      help='Harvest only samples submitted on this date. If set to R, look for the most recent job.')
    parser.add_option("-n", "--ncores", dest = "ncores",
                      default=20,
                      help='Number of cores on which to parralelise harvesting')
    parser.add_option("-F", "--ff", dest="apply_ff",
                      action="store_true", default=False,
                      help='whether or not to add fake factors to trees')
    parser.add_option("-c", "--convert", dest="convert_ntuple",
                      action="store_true", default=False,
                      help='whether or not to use convert_ntuple.py to convert the output tree')
    
    (options,args) = parser.parse_args()
    return options, args

def multithreadmap(f,X,ncores=20, **kwargs):
    """
    multithreading map of a function, default on 20 cpu cores.
    """
    func = partial(f, **kwargs)
    p=mp.Pool(ncores)
    Xout = p.map(func,X)
    p.terminate()
    return(Xout)

def find_dirs_in_dir(basepath, to_match="''"):
    os.system('xrdfs lyogrid06.in2p3.fr ls {} | grep {} > tmp.out'.format(basepath, to_match))
    matched_dirs = []
    with open('tmp.out') as f:
        for line in f.readlines():
            matched_dirs.append(line[:-1])
    return matched_dirs

def ask_for_user_selection(items):
    selection_done = (len(items) < 2)
    while not selection_done:
        print '    Warning, several matching directories:'
        for item in items:
            print '     ',item
        cutstring = raw_input('    Please enter a cut string on these names to select only one or pass all to get them all: ')
        print ''
        if cutstring == 'all' :
            selection_done = True
        else:
            items = [item for item in items if cutstring in item]
            selection_done = (len(items) < 2)
    return items

options, args = get_options()

matching_prod_label_dirs = find_dirs_in_dir('/dpm/in2p3.fr/home/cms/data/store/user/{}/heppyTrees/{}/'.format(options.username, options.cmssw_version), to_match=options.prod_label)

selected_dirs = []
for prod_label_dir in matching_prod_label_dirs:
    matching_comp_dirs = find_dirs_in_dir(prod_label_dir, to_match=options.cut_on_sample_names)
    for comp_dir in matching_comp_dirs:
        matched_dirs = find_dirs_in_dir(comp_dir)
        if options.select_date == 'R' :
            matched_dirs = [matched_dirs[-1]]
        else :
            matched_dirs = [dirname for dirname in matched_dirs if (options.select_date in matched_dirs or options.select_date is None) ]
            matched_dirs = ask_for_user_selection(matched_dirs)
        selected_dirs.extend(matched_dirs)

###formatting
selected_dirs = [dirname[dirname.find('store')-1:] for dirname in selected_dirs]

print 'Selected directories to harvest:'
for dirname in selected_dirs:
    print dirname

print ''
start_harvest = None
while start_harvest not in ['y','n']:
    start_harvest = raw_input('Harvest this list? [y/n]')
if start_harvest == 'y':
    print 'Starting to harvest.'
    multithreadmap(harvest, selected_dirs, ncores=options.ncores, subdir_pattern=options.subdir_pattern, tgz_pattern=options.tgz_pattern, apply_ff=options.apply_ff, convert_ntuple=options.convert_ntuple)
else:
    print 'Aborting.'


