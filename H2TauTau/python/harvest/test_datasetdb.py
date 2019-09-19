import unittest
import copy
import pprint
from datasetdb import DatasetDB
from dataset import Dataset
from test_dataset import dspath
from test_db import TestDB

# writedb = DatasetDB('writer')
# readdb = DatasetDB('reader')

class TestDatasetDB(TestDB):
 

    def test_1_mode(self):
        with self.assertRaises(ValueError): 
            DatasetDB('foo', 'thepass')

    def test_2_writedummy(self):
        '''test writer mode'''
        dsdb = self.__class__.db
        dsdb.insert('se',
                    {"path" : "aa", "name" : "bb", "subdir_pattern" : "*", 
                     "subdirs" : [ 0, 1 ], "tgz_pattern" : "*", "tgzs" : [ 2, 3 ]})
        data = dsdb.find('se',
                         {'path':'aa'})
        self.assertEqual(len(data),1)
        dsdb.remove('se', 
                    {'name':'bb'})

    def test_3_writeds(self):
        '''test writing a real dataset to the db'''
        dataset = Dataset(dspath)
        info = dataset.info()
        dsdb = self.__class__.db
        dsdb.remove('se', {'name':info['name']})
        dsdb.insert('se', info)
        tgzs = copy.deepcopy(info['tgzs'])

        def test_rinfo(infos): 
            self.assertEqual(len(rinfos), 1)
            rinfo = rinfos[0]
            del rinfo['_id']
            # pprint.pprint(rinfo)
            # pprint.pprint(info)
            self.assertDictEqual(rinfo, info)
            # self.assertEqual(len(rinfo['tgzs']['0000']), len(tgzs['0000']))
            

        # test that the information has been inserted. 
        # there was no such dataset before
        rinfos = dsdb.find('se', {'name':info['name']})
        test_rinfo(rinfos)

        # check find_by_name 
        rinfos = dsdb.find_by_name('se', info['name'])
        test_rinfo(rinfos)

        # find_by_name with a working pattern
        rinfos = dsdb.find_by_name('se', '.*')
        test_rinfo(rinfos)

        # and with a non-working one 
        rinfos = dsdb.find_by_name('se', 'foobar.*')
        self.assertEqual(len(rinfos), 0)

        # now test update KEEP AT THE END
        info['tgzs']['0000'].append('heppyOutput_666.tgz')
        dsdb.insert('se', info)
        rinfos = dsdb.find('se', {'name':info['name']})
        self.assertEqual(len(rinfos), 1)
        rinfo = rinfos[0]
        self.assertEqual(len(rinfo['tgzs']['0000']), len(tgzs['0000'])+1)
        
        # clean up 
        # writedb.remove('se', {'name':info['name']})

    def test_4_createcol(self):
        dsdb = self.__class__.db
        dsdb.insert('newcol', {'name':'foo', 'a':2})

if __name__ == '__main__': 
    unittest.main()
