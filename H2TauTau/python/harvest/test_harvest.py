import unittest 

from harvest import Harvester
from datasetdb import DatasetDB 

dsdb = DatasetDB()

class TestHarvest(unittest.TestCase): 

    def test_harvester(self): 
        harv = Harvester(dsdb)
        
if __name__ == '__main__':
    unittest.main()
