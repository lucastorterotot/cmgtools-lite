import unittest
import tempfile

from dataset import Dataset

class TestDatasetN(unittest.TestCase): 

    def test_read(self):
        '''test that a dataset can be read. does not fetch or unpack'''
        dspath = '/store/user/gtouquet/heppyTrees/190503/tt_DY_nominal/DYJetsToLL_M50/190505_112304'
        ds = Dataset(dspath)
        print(ds)
        self.assertEqual(ds.abspath('toto'), '/'.join([dspath,'toto']))
        self.assertEqual(len(ds.subdirs),1)
        self.assertEqual(ds.subdirs[0],'0000')
        self.assertTrue(len(ds.tgzs[ds.subdirs[0]])>1)
        # check the first tgz of the first subdir
        self.assertTrue(ds.tgzs[ds.subdirs[0]][0].endswith('.tgz'))

        

class TestDataset(unittest.TestCase):

    def setUp(self):
#         self.basepath = '/store/user/cbernet/heppyTrees/CMSSW_8_0_28_patch1/tauMu_2017_cfg/HiggsSUSYBB1000/180625_123805'
        self.basepath = '/store/user/gtouquet/heppyTrees/190503/tt_DY_nominal/DYJetsToLL_M50/190505_112304'
        self.ds = Dataset(self.basepath, tgzs='*_4?.tgz')

    def test_paths(self):
        self.assertEqual(self.ds.subdirs, ['0000'])
        self.assertEqual(len(self.ds.tgzs['0000']), 2)

    def test_unpack(self):
        ds = self.ds
        ds.unpack()
        print(ds)

    def test_patterns(self):
        ds =  Dataset(self.basepath,subdirs='')
        self.assertEqual(ds.subdirs, [])

if __name__ == '__main__':
    unittest.main()
