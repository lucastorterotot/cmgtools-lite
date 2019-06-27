import unittest 
import pprint 
import tempfile
import shutil
import os 
import subprocess
import time 

from harvest import Harvester
from datasetdb import DatasetDB 

dsdb = DatasetDB(mode='writer')
infos = [
    { "tgz_pattern" : "*", "name" : "190503%DY1JetsToLL_M50_LO%tt_DY_nominal", "sub_date" : "2019-05-05_13-02-17", "tgzs" : { "0000" : [ "heppyOutput_1.tgz", "heppyOutput_10.tgz", "heppyOutput_11.tgz", "heppyOutput_12.tgz", "heppyOutput_13.tgz", "heppyOutput_14.tgz", "heppyOutput_15.tgz", "heppyOutput_16.tgz", "heppyOutput_17.tgz", "heppyOutput_18.tgz", "heppyOutput_19.tgz", "heppyOutput_2.tgz", "heppyOutput_20.tgz", "heppyOutput_21.tgz", "heppyOutput_22.tgz", "heppyOutput_23.tgz", "heppyOutput_24.tgz", "heppyOutput_25.tgz", "heppyOutput_26.tgz", "heppyOutput_27.tgz", "heppyOutput_28.tgz", "heppyOutput_29.tgz", "heppyOutput_3.tgz", "heppyOutput_30.tgz", "heppyOutput_31.tgz", "heppyOutput_32.tgz", "heppyOutput_33.tgz", "heppyOutput_34.tgz", "heppyOutput_35.tgz", "heppyOutput_36.tgz", "heppyOutput_37.tgz", "heppyOutput_38.tgz", "heppyOutput_39.tgz", "heppyOutput_4.tgz", "heppyOutput_40.tgz", "heppyOutput_41.tgz", "heppyOutput_5.tgz", "heppyOutput_6.tgz", "heppyOutput_7.tgz", "heppyOutput_8.tgz", "heppyOutput_9.tgz" ] }, "subdirs" : [ "0000" ], "prod_date" : "190503", "sample" : "DY1JetsToLL_M50_LO", "sub_dir" : "/gridgroup/cms/touquet/crab_submission_dirs/crab_DY1JetsToLL_M50_LO_tt_DY_nominal/crab_DY1JetsToLL_M50_LO_190503_tt_DY_nominal_2019-05-05_13-02-17", "subdir_pattern" : "*", "write_date" : "190505_110450", "path" : "/store/user/gtouquet/heppyTrees/190503/tt_DY_nominal/DY1JetsToLL_M50_LO/190505_110450", "sample_version" : "tt_DY_nominal" },
    { "tgz_pattern" : "*", "name" : "190503%DY1JetsToLL_M50_LO_ext%tt_DY_nominal", "sub_date" : "2019-05-05_13-04-54", "tgzs" : { "0000" : [ "heppyOutput_1.tgz", "heppyOutput_10.tgz", "heppyOutput_11.tgz", "heppyOutput_12.tgz", "heppyOutput_13.tgz", "heppyOutput_14.tgz", "heppyOutput_15.tgz", "heppyOutput_16.tgz", "heppyOutput_17.tgz", "heppyOutput_18.tgz", "heppyOutput_19.tgz", "heppyOutput_2.tgz", "heppyOutput_20.tgz", "heppyOutput_21.tgz", "heppyOutput_22.tgz", "heppyOutput_23.tgz", "heppyOutput_24.tgz", "heppyOutput_25.tgz", "heppyOutput_26.tgz", "heppyOutput_27.tgz", "heppyOutput_28.tgz", "heppyOutput_29.tgz", "heppyOutput_3.tgz", "heppyOutput_30.tgz", "heppyOutput_31.tgz", "heppyOutput_32.tgz", "heppyOutput_33.tgz", "heppyOutput_4.tgz", "heppyOutput_5.tgz", "heppyOutput_6.tgz", "heppyOutput_7.tgz", "heppyOutput_8.tgz", "heppyOutput_9.tgz" ] }, "subdirs" : [ "0000" ], "prod_date" : "190503", "sample" : "DY1JetsToLL_M50_LO_ext", "sub_dir" : "/gridgroup/cms/touquet/crab_submission_dirs/crab_DY1JetsToLL_M50_LO_ext_tt_DY_nominal/crab_DY1JetsToLL_M50_LO_ext_190503_tt_DY_nominal_2019-05-05_13-04-54", "subdir_pattern" : "*", "write_date" : "190505_110725", "path" : "/store/user/gtouquet/heppyTrees/190503/tt_DY_nominal/DY1JetsToLL_M50_LO_ext/190505_110725", "sample_version" : "tt_DY_nominal" },
]

class TestHarvest(unittest.TestCase): 

    def setUp(self): 
        for info in infos:
            dsdb.insert('se', info)

    def tearDown(self): 
        for info in infos: 
            dsdb.remove('se', {'name':info['name']})

    def test_1_ds_info(self):
        '''test that dataset info can be readout with a regex'''
        harv = Harvester(dsdb)
        infos = harv.get_ds_infos('se', '.*DY1Jets.*')
        self.assertEqual(len(infos), 2)
        for info in infos: 
            self.assertTrue(len(info['tgzs']['0000'])>1)
                             
    def test_2_fetch(self): 
        harv = Harvester(dsdb)
        infos = harv.get_ds_infos('se', '.*DY1Jets.*_ext')
        outdir = tempfile.mkdtemp()
        # print(outdir)
        ntgzs = 2
        harv.fetch(infos[0], outdir, ntgzs)
        harv.unpack(infos[0], outdir, ntgzs)
        chunks = os.listdir(outdir)
        # pprint.pprint(chunks)
        self.assertListEqual(chunks, 
                             ['190503%DY1JetsToLL_M50_LO_ext%tt_DY_nominal_Chunk10',
                              '190503%DY1JetsToLL_M50_LO_ext%tt_DY_nominal_Chunk1']
                             )
        harv.hadd(outdir)
        results = os.listdir(outdir)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], '190503%DY1JetsToLL_M50_LO_ext%tt_DY_nominal')
        shutil.rmtree(outdir)

    def test_3_scp(self): 
        harv = Harvester(dsdb)
        srcdir = tempfile.mkdtemp()
        dummy_fname = 'foo'
        open('/'.join([srcdir, dummy_fname]),'w').close()

        # test local copy
        destdir = tempfile.mkdtemp()
        # print(srcdir)
        # print(destdir)
        harv.scp(srcdir, 'localhost:'+destdir)
        self.assertTrue(os.path.isfile('/'.join([destdir, 
                                                 os.path.basename(srcdir), 
                                                 dummy_fname])))
        
        # test copy to lyovis10 
        harv.scp(srcdir, 'localhost:'+destdir, '-P 2222')
        result = subprocess.check_output(
            'ssh -p 2222 localhost ls {}'.format(destdir).split()
            )
        self.assertEqual(result.strip(), dummy_fname)

        # cleaning up 
        shutil.rmtree(srcdir)
        shutil.rmtree(destdir)

    def test_4_harvest_one(self):
        harv = Harvester(dsdb)
        infos = harv.get_ds_infos('se', '.*DY1Jets.*_ext')
        destdir = '/data2/htt/unittests'
        info = infos[0]
        start = time.time()
        harv.harvest_one(info, destdir, ntgzs=2)
        # check that dataset exists on destination: 
        result = subprocess.check_output(
            'ssh -p 2222 localhost ls {}'.format(destdir).split()
            )
        self.assertEqual(result.strip(), info['name'])
        # check harvesting time in db
        hinfo = harv.get_ds_infos('harvested', info['name'])
        self.assertEqual(len(hinfo),1)
        self.assertTrue(hinfo[0]['harv_time']>start)

        
if __name__ == '__main__':
    unittest.main()
