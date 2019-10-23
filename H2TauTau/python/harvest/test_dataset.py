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
        self.maxDiff = None
        self.assertEqual(dataset.abspath('toto'), '/'.join([dspath,'toto']))
        info = dataset.info()
        self.assertEqual(len(info['subdirs']),1)
        self.assertEqual(info['subdirs'][0],'0000')
        self.assertTrue(len(info['tgzs'][info['subdirs'][0]])>1)
        # check the first tgz of the first subdir
        self.assertTrue(info['tgzs'][info['subdirs'][0]][0].endswith('.tgz'))
        test_dict = {'name': '190503%DYJetsToLL_M50%tt_DY_nominal',
                     'prod_date': '190503',
                     'sample': 'DYJetsToLL_M50',
                     'sample_version': 'tt_DY_nominal',
                     'path': '/store/user/gtouquet/heppyTrees/190503/tt_DY_nominal/DYJetsToLL_M50/190505_112304',
                     'subdir_pattern': '*',
                     'tgzs': {'0000': ['heppyOutput_43.tgz', 'heppyOutput_47.tgz']},
                     'subdirs': ['0000'],
                     'tgz_pattern': '*_4?.tgz',
                     'write_date': '190505_112304'
                     }
        pprint.pprint(dataset.info())
        pprint.pprint(test_dict)
        self.assertDictEqual(dataset.info(),test_dict)
        

    # def test_unpack(self):
    #     dest = 'tt_DY_nominal/DYJetsToLL_M50'
    #     if os.path.isdir(dest): 
    #         shutil.rmtree(dest)
    #     dataset.unpack()
    #     print(dataset)
        

if __name__ == '__main__':
    unittest.main()
