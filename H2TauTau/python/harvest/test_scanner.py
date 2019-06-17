import unittest
from scanner import Scanner
import pprint

class TestScanner(unittest.TestCase): 
    
    def test_subdirs(self):
        path = '/store/user/gtouquet/heppyTrees/190503'
        scanner = Scanner(path, '*tt_DY_Btagging*')
        # check that we can find at least one dataset
        self.assertTrue(len(scanner.datasets)>0)
        for ds in scanner.datasets: 
            self.assertTrue(len(ds.subdirs)>0)
        pprint.pprint(scanner.datasets)
        # check writing to db
        # scanner.writedb()
        


if __name__ == '__main__':
    unittest.main()
