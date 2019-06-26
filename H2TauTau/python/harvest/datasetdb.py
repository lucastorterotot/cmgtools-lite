import pymongo
import urllib
import sys 

class DatasetDB(object): 

    def __init__(self, mode='reader', db='datasets_unittests'):
        if mode not in ['reader', 'writer']: 
            raise( ValueError('mode must be either "reader" or "writer"') )
        pwd = raw_input('{} password:'.format(mode))
        self.client = pymongo.MongoClient(
            'mongodb://{}:{}@localhost/?authSource={}&authMechanism=MONGODB-CR'.format(
                mode, pwd, db
                ),
            27017
            )
        self.db = self.client[db]
        
    def insert(self, info, coll='se'): 
        self.db[coll].update({'name':info['name']}, 
                             info, 
                             upsert=True)

    def remove(self, query, coll='se'): 
        self.db[coll].remove(query)

    def find(self, query=None, coll='se'):
        if query is None: 
            query = {}
        return self.db[coll].find(query)

    def count(self, query=None, coll='se'): 
        if query is None: 
            query = {}
        return self.db[coll].count(query)
