import pymongo
import urllib
import sys 

user, passwd, db, coll = sys.argv[1:]
passwd = urllib.pathname2url(passwd)

print(user, passwd, db, coll)

client = pymongo.MongoClient(
    'mongodb://{}:{}@localhost/?authSource={}&authMechanism=MONGODB-CR'.format(user, passwd, db),
    27017
    )
coll = client[db][coll]

cursor = coll.find()
records = list(cursor)
print(records)

if user == 'writer':
    coll.insert({'a':1})

