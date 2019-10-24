import unittest 
import pprint 
import tempfile
import shutil
import os 
import subprocess
import time 
import copy

import harvest
from test_db import TestDB



class TestHarvest(TestDB): 

    def setUp(self): 
        super(TestHarvest, self).setUp()
        infos = [
            { "tgz_pattern" : "*", "name" : "190503%DY1JetsToLL_M50_LO%tt_DY_nominal", "sub_date" : "2019-05-05_13-02-17", "tgzs" : { "0000" : [ "heppyOutput_1.tgz", "heppyOutput_10.tgz", "heppyOutput_11.tgz", "heppyOutput_12.tgz", "heppyOutput_13.tgz", "heppyOutput_14.tgz", "heppyOutput_15.tgz", "heppyOutput_16.tgz", "heppyOutput_17.tgz", "heppyOutput_18.tgz", "heppyOutput_19.tgz", "heppyOutput_2.tgz", "heppyOutput_20.tgz", "heppyOutput_21.tgz", "heppyOutput_22.tgz", "heppyOutput_23.tgz", "heppyOutput_24.tgz", "heppyOutput_25.tgz", "heppyOutput_26.tgz", "heppyOutput_27.tgz", "heppyOutput_28.tgz", "heppyOutput_29.tgz", "heppyOutput_3.tgz", "heppyOutput_30.tgz", "heppyOutput_31.tgz", "heppyOutput_32.tgz", "heppyOutput_33.tgz", "heppyOutput_34.tgz", "heppyOutput_35.tgz", "heppyOutput_36.tgz", "heppyOutput_37.tgz", "heppyOutput_38.tgz", "heppyOutput_39.tgz", "heppyOutput_4.tgz", "heppyOutput_40.tgz", "heppyOutput_41.tgz", "heppyOutput_5.tgz", "heppyOutput_6.tgz", "heppyOutput_7.tgz", "heppyOutput_8.tgz", "heppyOutput_9.tgz" ] }, "subdirs" : [ "0000" ], "prod_date" : "190503", "sample" : "DY1JetsToLL_M50_LO", "sub_dir" : "/gridgroup/cms/touquet/crab_submission_dirs/crab_DY1JetsToLL_M50_LO_tt_DY_nominal/crab_DY1JetsToLL_M50_LO_190503_tt_DY_nominal_2019-05-05_13-02-17", "subdir_pattern" : "*", "write_date" : "190505_110450", "path" : "/store/user/gtouquet/heppyTrees/190503/tt_DY_nominal/DY1JetsToLL_M50_LO/190505_110450", "sample_version" : "tt_DY_nominal" },
            { "tgz_pattern" : "*", "name" : "190503%DY1JetsToLL_M50_LO_ext%tt_DY_nominal", "sub_date" : "2019-05-05_13-04-54", "tgzs" : { "0000" : [ "heppyOutput_1.tgz", "heppyOutput_10.tgz", "heppyOutput_11.tgz", "heppyOutput_12.tgz", "heppyOutput_13.tgz", "heppyOutput_14.tgz", "heppyOutput_15.tgz", "heppyOutput_16.tgz", "heppyOutput_17.tgz", "heppyOutput_18.tgz", "heppyOutput_19.tgz", "heppyOutput_2.tgz", "heppyOutput_20.tgz", "heppyOutput_21.tgz", "heppyOutput_22.tgz", "heppyOutput_23.tgz", "heppyOutput_24.tgz", "heppyOutput_25.tgz", "heppyOutput_26.tgz", "heppyOutput_27.tgz", "heppyOutput_28.tgz", "heppyOutput_29.tgz", "heppyOutput_3.tgz", "heppyOutput_30.tgz", "heppyOutput_31.tgz", "heppyOutput_32.tgz", "heppyOutput_33.tgz", "heppyOutput_4.tgz", "heppyOutput_5.tgz", "heppyOutput_6.tgz", "heppyOutput_7.tgz", "heppyOutput_8.tgz", "heppyOutput_9.tgz" ] }, "subdirs" : [ "0000" ], "prod_date" : "190503", "sample" : "DY1JetsToLL_M50_LO_ext", "sub_dir" : "/gridgroup/cms/touquet/crab_submission_dirs/crab_DY1JetsToLL_M50_LO_ext_tt_DY_nominal/crab_DY1JetsToLL_M50_LO_ext_190503_tt_DY_nominal_2019-05-05_13-04-54", "subdir_pattern" : "*", "write_date" : "190505_110725", "path" : "/store/user/gtouquet/heppyTrees/190503/tt_DY_nominal/DY1JetsToLL_M50_LO_ext/190505_110725", "sample_version" : "tt_DY_nominal" },
            {"name":"foo"}, 
            ]
        for info in infos: 
            self.__class__.db.insert('se', info)
        harvest.datasetdb = self.__class__.db

    def test_1_ds_info(self):
        '''test that dataset info can be readout and filtered'''
        # import pdb; pdb.set_trace()
        infos,done = harvest.get_ds_infos('.*DY1Jets.*')
        self.assertEqual(len(infos), 2)        
        self.assertEqual(len(done), 0)
        for info in infos: 
            self.assertTrue('path' in info)
            self.assertTrue(len(info['tgzs']['0000'])>1)
        # test that datasets already harvested are masked
        # create dummy harvesting information:
        harv_info = {
            'time': time.time(),
            'parent': None, 
            'dir': 'foo', 
            'tgzs': infos[1]['tgzs']
            }
        infos[1]['harvesting'] = harv_info
        harvest.datasetdb.insert('se', infos[1])
        infos,done = harvest.get_ds_infos('.*DY1Jets.*')
        print('selected')
        pprint.pprint(infos)
        print('done')
        pprint.pprint(done)
        self.assertEqual(len(infos), 1)
        self.assertEqual(len(done), 1)
        # add one more tgz to a sample that has already been harvested
        newinfo = copy.copy(done[0])
        newinfo['tgzs']['0000'].append('heppyOutput_666.tgz')
        harvest.datasetdb.insert('se', newinfo)
        infos2,done2 = harvest.get_ds_infos('.*DY1Jets.*')
        self.assertEqual(len(infos2), 2)
        self.assertEqual(len(done2), 0)        
        # add one more subdir
        newinfo = copy.copy(done[0])
        newinfo['tgzs']['0001'] = []
        infos2,done2 = harvest.get_ds_infos('.*DY1Jets.*')
        self.assertEqual(len(infos2), 2)
        self.assertEqual(len(done2), 0)        
         

                             
    def test_2_fetch(self): 
        infos,_ = harvest.get_ds_infos('.*DY1Jets.*_ext')
        outdir = tempfile.mkdtemp()
        # print(outdir)
        ntgzs = 2
        harvest.fetch(infos[0], outdir, ntgzs)
        harvest.unpack(infos[0], outdir, ntgzs)
        chunks = os.listdir(outdir)
        # pprint.pprint(chunks)
        self.assertListEqual(chunks, 
                             ['190503%DY1JetsToLL_M50_LO_ext%tt_DY_nominal_Chunk10',
                              '190503%DY1JetsToLL_M50_LO_ext%tt_DY_nominal_Chunk1']
                             )
        harvest.hadd(outdir)
        results = os.listdir(outdir)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], '190503%DY1JetsToLL_M50_LO_ext%tt_DY_nominal')
        shutil.rmtree(outdir)

    def test_3_scp(self): 
        srcdir = tempfile.mkdtemp()
        dummy_fname = 'foo'
        open('/'.join([srcdir, dummy_fname]),'w').close()

        # test local copy
        destdir = tempfile.mkdtemp()
        # print(srcdir)
        # print(destdir)
        harvest.scp(srcdir, 'localhost:'+destdir)
        self.assertTrue(os.path.isfile('/'.join([destdir, 
                                                 os.path.basename(srcdir), 
                                                 dummy_fname])))
        
        # test copy to lyovis10 
        harvest.scp(srcdir, 'localhost:'+destdir, '-P 2222')
        result = subprocess.check_output(
            'ssh -p 2222 localhost ls {}'.format(destdir).split()
            )
        self.assertEqual(result.strip(), dummy_fname)

        # cleaning up 
        shutil.rmtree(srcdir)
        shutil.rmtree(destdir)

    def test_4_harvest_one(self):
        infos,_ = harvest.get_ds_infos('.*DY1Jets.*_ext')
        destdir = '/gridgroup/cms/cbernet/unittests/single'
        info = infos[0]
        start = time.time()
        hinfo = harvest.harvest_one(info, destdir, ntgzs=2)
        harvest.datasetdb.insert('se', hinfo)
        # check that dataset exists on destination: 
        # result = subprocess.check_output(
        #     'ssh -p 2222 localhost ls {}'.format(destdir).split()
        #   )
        result = os.listdir(destdir)
        self.assertEqual(len(result),1)
        self.assertEqual(result[0], info['name'])
        # check harvesting time in db
        hinfo2 = harvest.datasetdb.find('se', {'name':info['name']})
        self.assertEqual(len(hinfo2),1)
        # pprint.pprint(hinfo2[0])
        self.assertTrue(hinfo2[0]['harvesting']['time']>start)

    def test_5_harvest_multi(self):
        '''test harvesting in multiprocessing'''
        infos,_ = harvest.get_ds_infos('.*')
        destdir = '/gridgroup/cms/cbernet/unittests/multi'
        harvest.harvest(infos, destdir, ntgzs=2, nworkers=2, delete='y')
        results = os.listdir(destdir)
        self.assertEqual(len(results), 2)

    def test_6_harvest_sequential(self):
        '''test that harvesting can be done in steps'''
        infos,_ = harvest.get_ds_infos('.*')
        destdir = '/gridgroup/cms/cbernet/unittests/multi'
        infos1 = infos[:1]
        infos2 = infos[1:2]
        harvest.harvest(infos1, destdir, ntgzs=2, nworkers=1, delete='y')
        harvest.harvest(infos2, destdir, ntgzs=2, nworkers=1, delete='n')
        results = os.listdir(destdir)
        self.assertEqual(len(results), 2)

        
if __name__ == '__main__':
    unittest.main()
