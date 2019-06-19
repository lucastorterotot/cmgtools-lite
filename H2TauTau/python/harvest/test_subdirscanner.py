import unittest
from subdirscanner import SubdirScanner
import pprint
import subprocess 

basedir = '/gridgroup/cms/touquet/crab_submission_dirs'

class TestSubdirScanner(unittest.TestCase):

    def test_find_dirs(self):
        '''test that directories can be found'''
        scanner = SubdirScanner()
        dirs = scanner._find_dirs(basedir, pattern='*HiggsSUSYGG3200*')
        pprint.pprint(dirs)
        self.assertTrue(len(dirs)>1)
        for path in dirs: 
            self.assertFalse(path.endswith('results'))
            self.assertFalse(path.endswith('inputs'))
                        
    def test_info(self): 
        scanner = SubdirScanner()
        dirs = [
            '/gridgroup/cms/touquet/crab_submission_dirs/crab_HiggsSUSYGG3200_tt_mssm_signals_METrecoil_resolution_up/crab_HiggsSUSYGG3200_190503_tt_mssm_signals_METrecoil_resolution_up_2019-05-17_07-51-36',
            '/gridgroup/cms/touquet/crab_submission_dirs/crab_HiggsSUSYGG3200_tt_mssm_signals_CMS_scale_j_RelativeBal_13TeV_up/crab_HiggsSUSYGG3200_190503_tt_mssm_signals_CMS_scale_j_RelativeBal_13TeV_up_2019-05-17_10-29-52',
            ]
        infos = scanner._extract_info(dirs)        
        self.assertEqual(len(infos),2)
        self.assertListEqual(infos, 
                             [{'base_sample': 'HiggsSUSYGG3200',
                               'prod_date': '190503',
                               'prod_name': 'tt_mssm_signals_METrecoil_resolution_up',
                               'sub_date': '2019-05-17_07-51-36',
                               'sub_dir': '/gridgroup/cms/touquet/crab_submission_dirs/crab_HiggsSUSYGG3200_tt_mssm_signals_METrecoil_resolution_up/crab_HiggsSUSYGG3200_190503_tt_mssm_signals_METrecoil_resolution_up_2019-05-17_07-51-36'},
                              {'base_sample': 'HiggsSUSYGG3200',
                               'prod_date': '190503',
                               'prod_name': 'tt_mssm_signals_CMS_scale_j_RelativeBal_13TeV_up',
                               'sub_date': '2019-05-17_10-29-52',
                               'sub_dir': '/gridgroup/cms/touquet/crab_submission_dirs/crab_HiggsSUSYGG3200_tt_mssm_signals_CMS_scale_j_RelativeBal_13TeV_up/crab_HiggsSUSYGG3200_190503_tt_mssm_signals_CMS_scale_j_RelativeBal_13TeV_up_2019-05-17_10-29-52'}]
                             )
        
    def test_scan(self):
        scanner = SubdirScanner()
        scanner.scan(basedir)
        self.assertEqual(len(scanner.dirs), len(scanner.infos))

    def test_find_os(self):
        print(subprocess.check_output('find {} -type d'.format(basedir).split()))
        


if __name__ == '__main__':
    unittest.main()
