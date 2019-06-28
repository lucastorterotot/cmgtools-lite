import unittest
from se_scanner import SEScanner
import pprint

class TestSEScanner(unittest.TestCase): 
    
    def test_1_duplicates(self): 
        paths = [
            '/store/user/gtouquet/heppyTrees/190503/tt_DY_Btagging_down/DY1JetsToLL_M50_LO/190505_153210',
            '/store/user/gtouquet/heppyTrees/190503/tt_DY_Btagging_down/DY1JetsToLL_M50_LO/190505_155301'
            ]
        scanner = SEScanner('dummy')
        infos = scanner._extract_info(paths)
        self.assertEqual(len(infos), len(paths))
        no_dupes = scanner._remove_duplicates(infos, 'write_date')
        self.assertEqual(len(no_dupes), 1)
        self.assertEqual(no_dupes[0]['write_date'], '190505_155301')

    def test_2_scan(self):
        '''test that we can scan'''
        path = '/store/user/gtouquet/heppyTrees/190503'
        scanner = SEScanner(path, '*tt_DY_Btagging_down*')
        scanner.scan()
        # check that we can find at least one dataset
        self.assertTrue(len(scanner.infos)>0)

if __name__ == '__main__':
    unittest.main()
