import unittest
from subdirscanner import SubdirScanner
from se_scanner import SEScanner
from test_db import TestDB
import pprint
import subprocess 

basedir = '/gridgroup/cms/touquet/crab_submission_dirs'

class TestSubdirScanner(TestDB):

    def setUp(self):
        super(TestSubdirScanner, self).setUp()
        self.maxDiff = None

    def test_info(self): 
        scanner = SubdirScanner('dummy', self.__class__.db)
        dirs = [
            '/gridgroup/cms/touquet/crab_submission_dirs/crab_HiggsSUSYGG3200_tt_mssm_signals_METrecoil_resolution_up/crab_HiggsSUSYGG3200_190503_tt_mssm_signals_METrecoil_resolution_up_2019-05-17_07-51-36',
            '/gridgroup/cms/touquet/crab_submission_dirs/crab_HiggsSUSYGG3200_tt_mssm_signals_CMS_scale_j_RelativeBal_13TeV_up/crab_HiggsSUSYGG3200_190503_tt_mssm_signals_CMS_scale_j_RelativeBal_13TeV_up_2019-05-17_10-29-52',
            ]
        infos = scanner._extract_info(dirs)        
        self.assertEqual(len(infos),2)
        self.assertListEqual(infos, 
                             [{'name':'190503%HiggsSUSYGG3200%tt_mssm_signals_METrecoil_resolution_up',
                               'njobs':1,
                               'sample': 'HiggsSUSYGG3200',
                               'prod_date': '190503',
                               'sample_version': 'tt_mssm_signals_METrecoil_resolution_up',
                               'sub_date': '2019-05-17_07-51-36',
                               'sub_dir': '/gridgroup/cms/touquet/crab_submission_dirs/crab_HiggsSUSYGG3200_tt_mssm_signals_METrecoil_resolution_up/crab_HiggsSUSYGG3200_190503_tt_mssm_signals_METrecoil_resolution_up_2019-05-17_07-51-36'},
                              {'name':'190503%HiggsSUSYGG3200%tt_mssm_signals_CMS_scale_j_RelativeBal_13TeV_up', 
                               'njobs':1,
                               'sample': 'HiggsSUSYGG3200',
                               'prod_date': '190503',
                               'sample_version': 'tt_mssm_signals_CMS_scale_j_RelativeBal_13TeV_up',
                               'sub_date': '2019-05-17_10-29-52',
                               'sub_dir': '/gridgroup/cms/touquet/crab_submission_dirs/crab_HiggsSUSYGG3200_tt_mssm_signals_CMS_scale_j_RelativeBal_13TeV_up/crab_HiggsSUSYGG3200_190503_tt_mssm_signals_CMS_scale_j_RelativeBal_13TeV_up_2019-05-17_10-29-52'}]
                             )
    def test_duplicates(self): 
        dirs = [
            '/gridgroup/cms/touquet/crab_submission_dirs/crab_DY3JetsToLL_M50_LO_tt_DY_TES_HadronicTau_3prong0pi0_down/crab_DY3JetsToLL_M50_LO_190503_tt_DY_TES_HadronicTau_3prong0pi0_down_2019-05-05_00-50-24',
            '/gridgroup/cms/touquet/crab_submission_dirs/crab_DY3JetsToLL_M50_LO_tt_DY_TES_HadronicTau_3prong0pi0_down/crab_DY3JetsToLL_M50_LO_190503_tt_DY_TES_HadronicTau_3prong0pi0_down_2019-05-05_22-45-56',
            '/gridgroup/cms/touquet/crab_submission_dirs/crab_DY4JetsToLL_M50_LO_tt_DY_CMS_scale_j_eta0to3_13TeV_up/crab_DY4JetsToLL_M50_LO_190503_tt_DY_CMS_scale_j_eta0to3_13TeV_up_2019-05-05_00-42-16',
            '/gridgroup/cms/touquet/crab_submission_dirs/crab_DY4JetsToLL_M50_LO_tt_DY_CMS_scale_j_eta0to3_13TeV_up/crab_DY4JetsToLL_M50_LO_190503_tt_DY_CMS_scale_j_eta0to3_13TeV_up_2019-05-05_14-10-23',
            '/gridgroup/cms/touquet/crab_submission_dirs/crab_HiggsSUSYGG400_tt_mssm_signals_nominal/crab_HiggsSUSYGG400_190503_tt_mssm_signals_nominal_2019-05-16_11-58-44'
            ] 
        scanner = SubdirScanner('dummy', self.__class__.db)
        infos = scanner._extract_info(dirs)
        no_dupes = scanner._remove_duplicates(infos, 'sub_date')
        # pprint.pprint(infos)
        # print('no dupes')
        # pprint.pprint(no_dupes)
        self.assertListEqual(
            no_dupes, 
            [{'name': '190503%DY3JetsToLL_M50_LO%tt_DY_TES_HadronicTau_3prong0pi0_down',
              'njobs': 1,
              'prod_date': '190503',
              'sample': 'DY3JetsToLL_M50_LO',
              'sample_version': 'tt_DY_TES_HadronicTau_3prong0pi0_down',
              'sub_date': '2019-05-05_22-45-56',
              'sub_dir': '/gridgroup/cms/touquet/crab_submission_dirs/crab_DY3JetsToLL_M50_LO_tt_DY_TES_HadronicTau_3prong0pi0_down/crab_DY3JetsToLL_M50_LO_190503_tt_DY_TES_HadronicTau_3prong0pi0_down_2019-05-05_22-45-56'},
             {'name': '190503%DY4JetsToLL_M50_LO%tt_DY_CMS_scale_j_eta0to3_13TeV_up',
              'njobs':4,
              'prod_date': '190503',
              'sample': 'DY4JetsToLL_M50_LO',
              'sample_version': 'tt_DY_CMS_scale_j_eta0to3_13TeV_up',
              'sub_date': '2019-05-05_14-10-23',
              'sub_dir': '/gridgroup/cms/touquet/crab_submission_dirs/crab_DY4JetsToLL_M50_LO_tt_DY_CMS_scale_j_eta0to3_13TeV_up/crab_DY4JetsToLL_M50_LO_190503_tt_DY_CMS_scale_j_eta0to3_13TeV_up_2019-05-05_14-10-23'},
             {'name': '190503%HiggsSUSYGG400%tt_mssm_signals_nominal',
              'njobs':1,
              'prod_date': '190503',
              'sample': 'HiggsSUSYGG400',
              'sample_version': 'tt_mssm_signals_nominal',
              'sub_date': '2019-05-16_11-58-44',
              'sub_dir': '/gridgroup/cms/touquet/crab_submission_dirs/crab_HiggsSUSYGG400_tt_mssm_signals_nominal/crab_HiggsSUSYGG400_190503_tt_mssm_signals_nominal_2019-05-16_11-58-44'}]
            ) 

    def test_scan(self):
        '''test the full scan'''
        scanner = SubdirScanner(basedir, self.__class__.db)
        scanner.scan()
        self.assertTrue(len(scanner.dirs) > 1)
        self.assertTrue(len(scanner.infos) < len(scanner.dirs) )

    def test_se_subdir_scan(self):
        '''check that the results of an se scan followed by a subdir scan are merged properly'''
        self.maxDiff=None
        path = '/store/user/gtouquet/heppyTrees/190503'
        scan_se = True
        # 190503%DY1JetsToLL_M50_LO_ext%tt_DY_Btagging_down

        scanner = SEScanner(path, self.__class__.db, '*tt_DY_Btagging_down*')
        infos = scanner.scan()
        selected = [info for info in infos 
                    if info['name']=='190503%DY1JetsToLL_M50_LO_ext%tt_DY_Btagging_down']
        self.assertEqual(len(selected), 1)
        scanner.writedb(selected)
        dirs = [
            '/gridgroup/cms/touquet/crab_submission_dirs/crab_DY1JetsToLL_M50_LO_ext_tt_DY_Btagging_down/crab_DY1JetsToLL_M50_LO_ext_190503_tt_DY_Btagging_down_2019-05-05_17-32-14'
            ]
        sdscanner = SubdirScanner('dummy', self.__class__.db)
        infos = sdscanner._extract_info(dirs)
        self.assertEqual(len(infos), 1)
        sdscanner.writedb(infos)
        # re-read and check merged information
        merged = selected[0]
        merged.update(infos[0])
        rinfos = sdscanner.database.find('se')
        self.assertEqual(len(infos), 1)
        rinfo = rinfos[0]
        # delete stuff that are automatically inserted by mongodb
        del rinfo['_id']
        self.assertDictEqual(rinfo, merged)
        
    def test_find_os(self):
        '''test that we can use the find command. split is necessary'''
        dirs = subprocess.check_output('find . -type d'.format(basedir).split())     
        self.assertTrue(len(dirs)>1)


    def test_find_njobs(self):
        '''test extraction of the number of jobs from the crab log'''
        sdscanner = SubdirScanner('dummy', self.__class__.db)
        path = '/gridgroup/cms/touquet/crab_submission_dirs/crab_W1JetsToLNu_LO_tt_generic_bg_Btagging_up/crab_W1JetsToLNu_LO_190503_tt_generic_bg_Btagging_up_2019-05-08_14-34-41'
        self.assertEqual( sdscanner._find_njobs(path), 54 )


if __name__ == '__main__':
    unittest.main()
