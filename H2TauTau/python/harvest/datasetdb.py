import pymongo
import urllib
import sys 

class DatasetDB(object): 

    def __init__(self, mode, pwd, db='datasets_unittests'):
        '''init connection with database.
        mode = reader(default) or writer 
        pwd = password
        db = dataset name (datasets_unittests by default)
        will ask for user password
        '''
        if mode not in ['reader', 'writer']: 
            raise( ValueError('mode must be either "reader" or "writer"') )
        self.client = pymongo.MongoClient(
            'mongodb://{}:{}@localhost/?authSource={}&authMechanism=MONGODB-CR'.format(
                mode, pwd, db
                ),
            27017
            )
        self.db = self.client[db]
        
    def insert(self, coll, info):
        '''insert or update a dataset info'''
        self.db[coll].update({'name':info['name']}, 
                             {'$set': info},
                             upsert=True)

    def remove(self, coll, query): 
        '''remove entries matching query in collection coll'''
        self.db[coll].remove(query)

    def find(self, coll, query=None):
        '''find entries matching query in collection coll'''
        if query is None: 
            query = {}
        return list(self.db[coll].find(query))

    def find_by_name(self, coll, regex): 
        '''find entries with a name matching the regex in coll'''
        query = {'name': {'$regex':regex}}
        return list(self.db[coll].find(query))

    def count(self, coll, query=None): 
        '''count entries matching query in collection coll'''
        if query is None: 
            query = {}
        return list(self.db[coll].count(query))

