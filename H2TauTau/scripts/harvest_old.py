#!/usr/bin/env python

from CMGTools.H2TauTau.harvest.harvest_old import harvest, get_options

if __name__ == '__main__':

    options, args = get_options()
    src = args[0]
    harvest(src, 
            subdir_pattern=options.subdir_pattern, 
            tgz_pattern=options.tgz_pattern, 
            apply_ff=options.apply_ff, 
            convert_ntuple=options.convert_ntuple)
