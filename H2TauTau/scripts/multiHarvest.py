from harvest import harvest
import os
from functools import partial
import multiprocessing as mp

def get_options():
    import os
    import sys
    from optparse import OptionParser
    usage = "usage: %prog [options] <src_dir>"
    parser = OptionParser(usage=usage)
    parser.add_option("-t", "--tgz-pattern", dest="tgz_pattern",
                      default='*',
                      help='tgz pattern')
    parser.add_option("-s", "--subdir-pattern", dest="subdir_pattern",
                      default='*',
                      help='subdir pattern')
    parser.add_option("-S", "--skim", dest="skim", action='store_true',
                      default=True,
                      help='whether or not to skim ntuples KIT style')
    parser.add_option("-u", "--user", dest = "username",
                      default=os.environ['USER'],
                      help='the username to be used to look for files.')
    parser.add_option("-V", "--CMSSW_VERSION", dest = "cmssw_version",
                      default=os.environ['CMSSW_VERSION'],
                      help='Version of CMSSW used to produce the samples.')
    parser.add_option("-l", "--prod_label", dest = "prod_label",
                      default='diTau_2018_modular_cfg',
                      help='Heppy cfg file used to produce the samples.')
    parser.add_option("-g", "--grep", dest = "cut_on_sample_names",
                      default="''",
                      help='Harvest only samples containing this string.')
    parser.add_option("-d", "--date", dest = "select_date",
                      default='',
                      help='Harvest only samples submitted on this date. If set to R, look for the most recent job.')
    parser.add_option("-c", "--cores", dest = "ncores",
                      default=20,
                      help='Number of cores on which to parralelise harvesting')
    
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

options, args = get_options()
os.system('xrdfs lyogrid06.in2p3.fr ls /dpm/in2p3.fr/home/cms/data/store/user/{}/heppyTrees/{}/{}/ | grep {} > files.out'.format(options.username, options.cmssw_version, options.prod_label, options.cut_on_sample_names))

# Select directories
selected_fcompos = set()
print ''
print 'Selecting directories: '+os.popen('cat files.out | wc -l').readline()[:-1]+' directories to process.'
Ndir = 0
with open('files.out') as f:
    for line in f.readlines():
        Ndir += 1
        print '  '+str(Ndir)+'/'+os.popen('cat files.out | wc -l').readline()[:-1]
        component = line[line.rfind('/')+1:-1]
        os.system('xrdfs lyogrid06.in2p3.fr ls /dpm/in2p3.fr/home/cms/data/store/user/gtouquet/heppyTrees/CMSSW_9_4_11_cand1/diTau_2018_modular_cfg/{}/ > {}.out'.format(component,component))
        with open('{}.out'.format(component)) as fcomponent:
            cutstring = None
            if options.select_date == 'R' :
                matching_fcompo = [fcomponent.readlines()[-1]]
            else :
                matching_fcompo = [line for line in fcomponent.readlines() if options.select_date in line]
                while len(matching_fcompo) > 1:
                    print '    Warning, several matching directories for component '+component+':'
                    for compo in matching_fcompo :
                        print '     '+compo[:-1]
                    cutstring = raw_input('    Please enter a cut string on these names to select only one or pass all to get them all:')
                    print ''
                    if cutstring == 'all' :
                        for fcompo in matching_fcompo :
                            selected_fcompos.add(fcompo)
                        matching_fcompo = []
                    else :
                        matching_fcompo = [line for line in matching_fcompo if cutstring in line]
            if cutstring is not 'all' :
                if len(matching_fcompo) == 0 :
                    print '  Warning, no matching files for component '+component
                else :
                    selected_fcompos.add(matching_fcompo[0])
            os.system('rm '+component+'.out')
os.system('rm files.out')

# Build list to harvest
to_harvest = []
print ''
for fcompo in selected_fcompos :
    to_harvest.append(fcompo[fcompo.find('store')-1:-1])
to_harvest.sort()
print 'Selected directories to harvest:'
for to_harvest_i in to_harvest:
    print '  '+to_harvest_i

print ''
start_harvest = None
while start_harvest not in ['y','n']:
    start_harvest = raw_input('Harvest this list? [y/n]')
if start_harvest == 'y':
    print 'Starting to harvest.'
    # multithreadmap(harvest, to_harvest, ncores=1+0*options.ncores, subdir_pattern=optionssubdir_pattern, tgz_pattern=options.tgz_pattern, skim=options.skim)
    # harvest(to_harvest[0])
else:
    print 'Aborting.'


