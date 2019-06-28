import unittest
from subdirscanner import SubdirScanner
import pprint
import subprocess 

basedir = '/gridgroup/cms/touquet/crab_submission_dirs'

class TestSubdirScanner(unittest.TestCase):

    # @unittest.skip('already tested in test_scan, and too long')
    # def test_find_dirs(self):
    #     '''test that directories can be found'''
    #     scanner = SubdirScanner('dummy')
    #     dirs = scanner._find_dirs(basedir, pattern='*HiggsSUSYGG3200*')
    #     pprint.pprint(dirs)
    #     self.assertTrue(len(dirs)>1)
    #     for path in dirs: 
    #         self.assertFalse(path.endswith('results'))
    #         self.assertFalse(path.endswith('inputs'))
                        
    def test_info(self): 
        scanner = SubdirScanner('dummy')
        dirs = [
            '/gridgroup/cms/touquet/crab_submission_dirs/crab_HiggsSUSYGG3200_tt_mssm_signals_METrecoil_resolution_up/crab_HiggsSUSYGG3200_190503_tt_mssm_signals_METrecoil_resolution_up_2019-05-17_07-51-36',
            '/gridgroup/cms/touquet/crab_submission_dirs/crab_HiggsSUSYGG3200_tt_mssm_signals_CMS_scale_j_RelativeBal_13TeV_up/crab_HiggsSUSYGG3200_190503_tt_mssm_signals_CMS_scale_j_RelativeBal_13TeV_up_2019-05-17_10-29-52',
            ]
        infos = scanner._extract_info(dirs)        
        self.assertEqual(len(infos),2)
        self.assertListEqual(infos, 
                             [{'name':'190503%HiggsSUSYGG3200%tt_mssm_signals_METrecoil_resolution_up',
                               'sample': 'HiggsSUSYGG3200',
                               'prod_date': '190503',
                               'sample_version': 'tt_mssm_signals_METrecoil_resolution_up',
                               'sub_date': '2019-05-17_07-51-36',
                               'sub_dir': '/gridgroup/cms/touquet/crab_submission_dirs/crab_HiggsSUSYGG3200_tt_mssm_signals_METrecoil_resolution_up/crab_HiggsSUSYGG3200_190503_tt_mssm_signals_METrecoil_resolution_up_2019-05-17_07-51-36'},
                              {'name':'190503%HiggsSUSYGG3200%tt_mssm_signals_CMS_scale_j_RelativeBal_13TeV_up', 
                               'sample': 'HiggsSUSYGG3200',
                               'prod_date': '190503',
                               'sample_version': 'tt_mssm_signals_CMS_scale_j_RelativeBal_13TeV_up',
                               'sub_date': '2019-05-17_10-29-52',
                               'sub_dir': '/gridgroup/cms/touquet/crab_submission_dirs/crab_HiggsSUSYGG3200_tt_mssm_signals_CMS_scale_j_RelativeBal_13TeV_up/crab_HiggsSUSYGG3200_190503_tt_mssm_signals_CMS_scale_j_RelativeBal_13TeV_up_2019-05-17_10-29-52'}]
                             )

    # def test_writedb(self):
    #     scanner = SubdirScanner('dummy')
    #     dirs = [
    #         '/gridgroup/cms/touquet/crab_submission_dirs/crab_HiggsSUSYGG3200_tt_mssm_signals_METrecoil_resolution_up/crab_HiggsSUSYGG3200_190503_tt_mssm_signals_METrecoil_resolution_up_2019-05-17_07-51-36',
    #         '/gridgroup/cms/touquet/crab_submission_dirs/crab_HiggsSUSYGG3200_tt_mssm_signals_CMS_scale_j_RelativeBal_13TeV_up/crab_HiggsSUSYGG3200_190503_tt_mssm_signals_CMS_scale_j_RelativeBal_13TeV_up_2019-05-17_10-29-52',
    #         ]
    #     infos = scanner._extract_info(dirs)
    #     for info in infos: 
    #         info['name']='test'
    #     scanner.writedb(infos)
    #     scanner.database.remove({'name':'test'}) 

    def test_duplicates(self): 
        dirs = [
            '/gridgroup/cms/touquet/crab_submission_dirs/crab_DY3JetsToLL_M50_LO_tt_DY_TES_HadronicTau_3prong0pi0_down/crab_DY3JetsToLL_M50_LO_190503_tt_DY_TES_HadronicTau_3prong0pi0_down_2019-05-05_00-50-24',
            '/gridgroup/cms/touquet/crab_submission_dirs/crab_DY3JetsToLL_M50_LO_tt_DY_TES_HadronicTau_3prong0pi0_down/crab_DY3JetsToLL_M50_LO_190503_tt_DY_TES_HadronicTau_3prong0pi0_down_2019-05-05_22-45-56',
            '/gridgroup/cms/touquet/crab_submission_dirs/crab_DY4JetsToLL_M50_LO_tt_DY_CMS_scale_j_eta0to3_13TeV_up/crab_DY4JetsToLL_M50_LO_190503_tt_DY_CMS_scale_j_eta0to3_13TeV_up_2019-05-05_00-42-16',
            '/gridgroup/cms/touquet/crab_submission_dirs/crab_DY4JetsToLL_M50_LO_tt_DY_CMS_scale_j_eta0to3_13TeV_up/crab_DY4JetsToLL_M50_LO_190503_tt_DY_CMS_scale_j_eta0to3_13TeV_up_2019-05-05_14-10-23',
            '/gridgroup/cms/touquet/crab_submission_dirs/crab_HiggsSUSYGG400_tt_mssm_signals_nominal/crab_HiggsSUSYGG400_190503_tt_mssm_signals_nominal_2019-05-16_11-58-44'
            ] 
        scanner = SubdirScanner('dummy')
        infos = scanner._extract_info(dirs)
        no_dupes = scanner._remove_duplicates(infos, 'sub_date')
        # pprint.pprint(infos)
        # print('no dupes')
        # pprint.pprint(no_dupes)
        self.assertListEqual(
            no_dupes, 
            [{'name': '190503%DY3JetsToLL_M50_LO%tt_DY_TES_HadronicTau_3prong0pi0_down',
              'prod_date': '190503',
              'sample': 'DY3JetsToLL_M50_LO',
              'sample_version': 'tt_DY_TES_HadronicTau_3prong0pi0_down',
              'sub_date': '2019-05-05_22-45-56',
              'sub_dir': '/gridgroup/cms/touquet/crab_submission_dirs/crab_DY3JetsToLL_M50_LO_tt_DY_TES_HadronicTau_3prong0pi0_down/crab_DY3JetsToLL_M50_LO_190503_tt_DY_TES_HadronicTau_3prong0pi0_down_2019-05-05_22-45-56'},
             {'name': '190503%DY4JetsToLL_M50_LO%tt_DY_CMS_scale_j_eta0to3_13TeV_up',
              'prod_date': '190503',
              'sample': 'DY4JetsToLL_M50_LO',
              'sample_version': 'tt_DY_CMS_scale_j_eta0to3_13TeV_up',
              'sub_date': '2019-05-05_14-10-23',
              'sub_dir': '/gridgroup/cms/touquet/crab_submission_dirs/crab_DY4JetsToLL_M50_LO_tt_DY_CMS_scale_j_eta0to3_13TeV_up/crab_DY4JetsToLL_M50_LO_190503_tt_DY_CMS_scale_j_eta0to3_13TeV_up_2019-05-05_14-10-23'},
             {'name': '190503%HiggsSUSYGG400%tt_mssm_signals_nominal',
              'prod_date': '190503',
              'sample': 'HiggsSUSYGG400',
              'sample_version': 'tt_mssm_signals_nominal',
              'sub_date': '2019-05-16_11-58-44',
              'sub_dir': '/gridgroup/cms/touquet/crab_submission_dirs/crab_HiggsSUSYGG400_tt_mssm_signals_nominal/crab_HiggsSUSYGG400_190503_tt_mssm_signals_nominal_2019-05-16_11-58-44'}]
            ) 

    def test_scan(self):
        '''test the full scan'''
        scanner = SubdirScanner(basedir)
        scanner.scan()
        self.assertTrue(len(scanner.dirs) > 1)
        self.assertTrue(len(scanner.infos) < len(scanner.dirs) )

    def test_find_os(self):
        '''test that we can use the find command. split is necessary'''
        dirs = subprocess.check_output('find . -type d'.format(basedir).split())     
        self.assertTrue(len(dirs)>1)


if __name__ == '__main__':
    unittest.main()
