import unittest
from getpass import getpass
from datasetdb import DatasetDB 

pwd = getpass()

class TestDB(unittest.TestCase): 
    '''base unittest for tests that need DatasetDB. 
    The password needs to be entered only once
    Manages database cleanup after each test.
    '''

    @classmethod
    def setUpClass(cls): 
        cls.db = DatasetDB('writer', pwd, db='datasets_unittests')

    def tearDown(self): 
        self.__class__.db.remove('se', {})
        self.__class__.db.remove('harvested', {})
        
@unittest.skip('dummy test')
class Dummy(TestDB):
    def test_1(self):
        self.assertTrue(self.__class__.pwd == 'blah')

if __name__ == "__main__": 
    unittest.main()
