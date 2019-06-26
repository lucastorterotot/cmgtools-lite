import unittest
import copy
import pprint
from datasetdb import DatasetDB
from dataset import Dataset
from test_dataset import dspath


writedb = DatasetDB('writer')
readdb = DatasetDB('reader')

class TestDatasetDB(unittest.TestCase):
    
    def test_999_read(self): 
        '''test that a test entry can be read, in reader mode'''
        data = readdb.find('se')
        self.assertEqual(len(data),0)

    def test_2_writedummy(self):
        '''test writer mode'''
        dsdb = writedb
        dsdb.insert('se',
                    {"path" : "aa", "name" : "bb", "subdir_pattern" : "*", 
                     "subdirs" : [ 0, 1 ], "tgz_pattern" : "*", "tgzs" : [ 2, 3 ]})
        data = dsdb.find('se',
                         {'path':'aa'})
        self.assertEqual(len(data),1)
        dsdb.remove('se', 
                    {'name':'bb'})
        with self.assertRaises(ValueError): 
            DatasetDB('foo')

    def test_3_writeds(self):
        '''test writing a real dataset to the db'''
        dataset = Dataset(dspath)
        info = dataset.info()
        writedb.remove('se', {'name':info['name']})
        writedb.insert('se', info)
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
        rinfos = writedb.find('se', {'name':info['name']})
        test_rinfo(rinfos)

        # check find_by_name 
        rinfos = writedb.find_by_name('se', info['name'])
        test_rinfo(rinfos)

        # find_by_name with a working pattern
        rinfos = writedb.find_by_name('se', '.*')
        test_rinfo(rinfos)

        # and with a non-working one 
        rinfos = writedb.find_by_name('se', 'foobar.*')
        self.assertEqual(len(rinfos), 0)

        # now test update KEEP AT THE END
        info['tgzs']['0000'].append('heppyOutput_666.tgz')
        writedb.insert('se', info)
        rinfos = writedb.find('se', {'name':info['name']})
        self.assertEqual(len(rinfos), 1)
        rinfo = rinfos[0]
        self.assertEqual(len(rinfo['tgzs']['0000']), len(tgzs['0000'])+1)
        
        
        # clean up 
        writedb.remove('se', {'name':info['name']})
        

if __name__ == '__main__': 
    unittest.main()
