import unittest
from se_scanner import SEScanner
import pprint

class TestSEScanner(unittest.TestCase): 
    
    def test_1(self):
        '''test that we can scan'''
        path = '/store/user/gtouquet/heppyTrees/190503'
        scanner = SEScanner(path, '*tt_DY_Btagging_down*')
        scanner.scan()
        # check that we can find at least one dataset
        self.assertTrue(len(scanner.infos)>0)

if __name__ == '__main__':
    unittest.main()
