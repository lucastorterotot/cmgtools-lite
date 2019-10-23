import unittest
import pymongo

@unittest.skip('mongo already tested in test_datasetdb')
class TestMongo(unittest.TestCase): 

    def setUp(self):
        self.db, self.coll = 'test', 'coll'
        self.to_insert =  {'a':1}
        
    def test_1_writer(self):
        # test readWrite
        rpwd = raw_input('reader password:')
        wpwd = raw_input('writer password:')
        client = pymongo.MongoClient(
            'mongodb://{}:{}@localhost/?authSource={}&authMechanism=MONGODB-CR'.format(
                'writer', wpwd, self.db
                ),
            27017
            )
        coll = client[self.db][self.coll]
        coll.remove({})
        coll.insert(self.to_insert)
        data = list(coll.find())
        self.assertEqual(len(data), 1)
        self.assertDictEqual(data[0], self.to_insert)

        # test read
        client = pymongo.MongoClient(
            'mongodb://{}:{}@localhost/?authSource={}&authMechanism=MONGODB-CR'.format(
                'reader', rpwd, self.db
                ),
            27017
            )
        coll = client[self.db][self.coll]
        data = list(coll.find())
        self.assertEqual(len(data), 1)
        self.assertDictEqual(data[0], self.to_insert)

        # test that we cannot write with the reader 
        with self.assertRaises(pymongo.errors.OperationFailure):
            coll.insert({'willfail': 2})


if __name__ == '__main__':
        
    unittest.main()

