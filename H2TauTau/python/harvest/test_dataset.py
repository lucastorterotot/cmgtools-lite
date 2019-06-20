import unittest
import tempfile
import os 
import shutil
import pprint
from dataset import Dataset

dspath = '/store/user/gtouquet/heppyTrees/190503/tt_DY_nominal/DYJetsToLL_M50/190505_112304'
# selecting only part of the tgzs, for faster testing of the unpacking
dataset = Dataset(dspath, tgzs='*_4?.tgz')

class TestDataset(unittest.TestCase): 

    def test_read(self):
        '''test that a dataset can be read. does not fetch or unpack'''
        print(dataset)
        self.assertEqual(dataset.abspath('toto'), '/'.join([dspath,'toto']))
        self.assertEqual(len(dataset.subdirs),1)
        self.assertEqual(dataset.subdirs[0],'0000')
        self.assertTrue(len(dataset.tgzs[dataset.subdirs[0]])>1)
        # check the first tgz of the first subdir
        self.assertTrue(dataset.tgzs[dataset.subdirs[0]][0].endswith('.tgz'))
        pprint.pprint(dataset.info())
        self.assertDictEqual(dataset.info(),
                             {'name': '190503%DYJetsToLL_M50%tt_DY_nominal',
                              'prod_date': '190503',
                              'sample': 'DYJetsToLL_M50',
                              'sample_version': 'tt_DY_nominal',
                              'se_path': '/store/user/gtouquet/heppyTrees/190503/tt_DY_nominal/DYJetsToLL_M50/190505_112304',
                              'subdir_pattern': '*',
                              'subdirs': ['0000'],
                              'tgz_pattern': '*_4?.tgz',
                              'tgzs': {'0000': ['heppyOutput_43.tgz', 'heppyOutput_47.tgz']}}
                             )
         

    def test_unpack(self):
        dest = 'tt_DY_nominal/DYJetsToLL_M50'
        if os.path.isdir(dest): 
            shutil.rmtree(dest)
        dataset.unpack()
        print(dataset)
        

if __name__ == '__main__':
    unittest.main()
