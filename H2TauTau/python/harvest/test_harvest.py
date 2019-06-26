import unittest 
import pprint 

from harvest import Harvester
from datasetdb import DatasetDB 

dsdb = DatasetDB()

class TestHarvest(unittest.TestCase): 

    def test_harvester(self): 
        harv = Harvester(dsdb)
        infos = harv.get_ds_infos()
        pprint.pprint(infos)
        
    def test_harvester2(self): 
        harv = Harvester(dsdb)

if __name__ == '__main__':
    unittest.main()
