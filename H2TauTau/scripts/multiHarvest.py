from harvest import harvest
import os
from functools import partial
import multiprocessing as mp


def multithreadmap(f,X,ncores=20, **kwargs):
    """
    multithreading map of a function, default on 20 cpu cores.
    """
    func = partial(f, **kwargs)
    p=mp.Pool(ncores)
    Xout = p.map(func,X)
    p.terminate()
    return(Xout)


# os.system('rm -rf multiharvesttmp')

# os.system('mkdir multiharvesttmp')

os.system('xrdfs lyogrid06.in2p3.fr ls /dpm/in2p3.fr/home/cms/data/store/user/gtouquet/heppyTrees/CMSSW_9_4_11_cand1/diTau_2018_modular_cfg/ > files.out')

to_harvest = []

samples_to_harvest = ['Embedded2017B_tt','Embedded2017C_tt','Embedded2017D_tt','Embedded2017E_tt','Embedded2017F_tt']

with open('files.out') as f:
    for line in f.readlines():
        component = line[line.rfind('/')+1:-1]
        os.system('xrdfs lyogrid06.in2p3.fr ls /dpm/in2p3.fr/home/cms/data/store/user/gtouquet/heppyTrees/CMSSW_9_4_11_cand1/diTau_2018_modular_cfg/{}/ > {}.out'.format(component,component))
        with open('{}.out'.format(component)) as fcomponent:
            latest = fcomponent.readlines()
            if samples_to_harvest == [] or component in samples_to_harvest:
                to_harvest.append(latest[-1][latest[-1].find('store')-1:-1])

# to_harvest = to_harvest[-1:]
multithreadmap(harvest, to_harvest, skim=True)
# harvest(to_harvest[0])
