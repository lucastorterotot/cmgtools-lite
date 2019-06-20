import pymongo
import urllib
import sys 

class DatasetDB(object): 

    def __init__(self, mode='reader', db='datasets', coll='se'):
        if mode not in ['reader', 'writer']: 
            raise( ValueError('mode must be either "reader" or "writer"') )
        pwd = raw_input('{} password:'.format(mode))
        self.client = pymongo.MongoClient(
            'mongodb://{}:{}@localhost/?authSource={}&authMechanism=MONGODB-CR'.format(
                mode, pwd, db
                ),
            27017
            )
        self.coll = self.client[db][coll]
        
    def insert(self,info): 
        self.coll.update({'name':info['name']}, 
                         info, 
                         upsert=True)

    def remove(self, query): 
        self.coll.remove(query)
