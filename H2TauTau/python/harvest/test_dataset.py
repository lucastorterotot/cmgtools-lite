import unittest
import tempfile
import os 
import shutil

from dataset import Dataset

class TestDataset(unittest.TestCase): 

    def setUp(self):
        self.dspath = '/store/user/gtouquet/heppyTrees/190503/tt_DY_nominal/DYJetsToLL_M50/190505_112304'
        # this should select two tgzs: 
        self.ds = Dataset(self.dspath, tgzs='*_4?.tgz')

    def test_read(self):
        '''test that a dataset can be read. does not fetch or unpack'''
        ds = self.ds
        print(ds)
        self.assertEqual(ds.abspath('toto'), '/'.join([self.dspath,'toto']))
        self.assertEqual(len(ds.subdirs),1)
        self.assertEqual(ds.subdirs[0],'0000')
        self.assertTrue(len(ds.tgzs[ds.subdirs[0]])>1)
        # check the first tgz of the first subdir
        self.assertTrue(ds.tgzs[ds.subdirs[0]][0].endswith('.tgz'))

    def test_unpack(self):
        ds = self.ds
        dest = 'tt_DY_nominal/DYJetsToLL_M50'
        if os.path.isdir(dest): 
            shutil.rmtree(dest)
        ds.unpack()
        print(ds)
        

if __name__ == '__main__':
    unittest.main()
