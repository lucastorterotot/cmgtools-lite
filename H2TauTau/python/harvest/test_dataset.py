import unittest
import tempfile
import os 
import shutil

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
        self.assertDictEqual(dataset.info(), 
                             {'subdir_pattern': '*', 
                              'tgzs': {'0000': ['heppyOutput_43.tgz', 'heppyOutput_47.tgz']}, 
                              'path': '/store/user/gtouquet/heppyTrees/190503/tt_DY_nominal/DYJetsToLL_M50/190505_112304',
                              'tgz_pattern': '*_4?.tgz', 
                              'subdirs': ['0000'], 
                              'name': 'DYJetsToLL_M50'})
        


    def test_unpack(self):
        dest = 'tt_DY_nominal/DYJetsToLL_M50'
        if os.path.isdir(dest): 
            shutil.rmtree(dest)
        dataset.unpack()
        print(dataset)
        

if __name__ == '__main__':
    unittest.main()
