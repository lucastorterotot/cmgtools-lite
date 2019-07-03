import unittest 
import shutil
import os
import pprint

import postproc

from test_db import TestDB

class TestPostProc(TestDB): 

    def setUp(self):
        super(TestPostProc, self).setUp()
        postproc.dataset_db = self.__class__.db
        self.__class__.db.insert(
            'se', 
            {
                "name" : "190503%TBar_tch%tt_generic_bg_METrecoil_response_down",
                "subdir_pattern" : "*",
                "tgzs" : {
                    "0000" : [
                        "heppyOutput_1.tgz",
                        "heppyOutput_2.tgz",
                        "heppyOutput_3.tgz"
                        ]
                    },
                "subdirs" : [
                    "0000"
                    ],
                "prod_date" : "190503",
                "sample" : "TBar_tch",
                "write_date" : "190507_093219",
                "path" : "/store/user/gtouquet/heppyTrees/190503/tt_generic_bg_METrecoil_response_down/TBar_tch/190507_093219",
                "tgz_pattern" : "*",
                "sample_version" : "tt_generic_bg_METrecoil_response_down",
                "sub_date" : "2019-05-07_11-28-15",
                "sub_dir" : "/gridgroup/cms/touquet/crab_submission_dirs/crab_TBar_tch_tt_generic_bg_METrecoil_response_down/crab_TBar_tch_190503_tt_generic_bg_METrecoil_response_down_2019-05-07_11-28-15",
                "njobs" : 3,
                "tiers" : { "T1" : { "dir" : "/home/cms/cbernet/CMS/HTauTau/2017/CMSSW_9_4_11_cand1/src/CMGTools/H2TauTau/python/harvest/test_data"
                                     }
                            }
                }
            )
        
    def test_load_script(self): 
        func, meta = postproc.load_script('test_macros/dummy.py')
        self.assertEqual( func('bar'), ('foo', 'subdir/bar') )
        self.assertDictEqual( meta,  {'foo' : 'bar'} )  
    
    def test_get_datasets_nodb(self):
        with self.assertRaises(ValueError): 
            postproc.dataset_db = None
            postproc.get_datasets('.*')

    def test_get_datasets(self):
        infos = postproc.get_datasets('TBar_tch')
        self.assertEqual(len(infos), 1)
        
    def test_prepare_output(self):
        outdspath =  'test_data/outdir'
        postproc.prepare_output_dataset('test_data/190503%HiggsSUSYBB900%tt_mssm_signals_nominal', 
                                        outdspath)
        rootfiles = []
        norootfiles = []
        for _,_,files in os.walk(outdspath): 
            for f in files: 
                if f.endswith('.root'):
                    rootfiles.append(f)
                else:
                    norootfiles.append(f)
        self.assertEqual(len(rootfiles), 0)
        self.assertEqual(len(norootfiles), 34)
        shutil.rmtree(outdspath)
            
    def test_process_dataset(self): 
        outdir = 'test_data/outdir'
        if os.path.isdir(outdir): 
            shutil.rmtree(outdir)
        os.mkdir(outdir)
        infos = postproc.get_datasets('TBar_tch')
        info = infos[0]
        self.assertEqual(len(infos), 1)
        func, meta = postproc.load_script('test_macros/copy.py')
        new_info = postproc.process_dataset(info, 'T1', func, meta, outdir, 'T2')
        # check that the new dataset directory exists
        dsname = info['name']
        dsdir = os.path.join(outdir, dsname)
        self.assertTrue( os.path.isdir(dsdir) )
        # check that it contains only one root file, the one we created
        rootfiles = []
        for _,_,files in os.walk(dsdir): 
            for f in files: 
                if f.endswith('.root'):
                    rootfiles.append(f)
        self.assertEqual(len(rootfiles), 1)
        # check that new info is correct
        # contains the new tier
        self.assertDictEqual(
            new_info['tiers']['T2'], 
            {'foo':'bar', 
             'dir': os.path.abspath(outdir)
             } 
            )
        # and is otherwise identical to old info
        del new_info['tiers']['T2']
        self.assertDictEqual(new_info, info)
        shutil.rmtree(outdir) 

if __name__ == '__main__':
    unittest.main()
